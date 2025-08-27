const ALLOWED_REFERRERS = [
    'http://.pcl2.server/',
    'http://.open.pcl2.server/',
    'http://.pcl2.open.server/',
    'https://.pcl2.server/',
    'https://.open.pcl2.server/',
    'https://.pcl2.open.server/'
];


const isValidUA = (ua) => ua && ua.includes('PCL2/');

const isValidReferer = (referer) => {
    if (!referer) return false;
    return ALLOWED_REFERRERS.some(domain => {
        const clean = domain.replace(/^https?:\/\//, '').replace(/^\./, '');
        return referer.includes(clean);
    });
};

// === 内联：KV 访问逻辑（替代 require）===
/**
 * 从 KV 获取计数器数据
 * @param {string} key - 存储键
 * @param {Object} env - Worker 环境变量（包含 ACCESS_COUNTER）
 * @returns {Object} { counter, timestamps }
 */
async function getCounter(key, env) {
    const stored = await env.ACCESS_COUNTER.get(key);
    if (!stored) {
        return { counter: 0, timestamps: [] };
    }
    try {
        return JSON.parse(stored);
    } catch (e) {
        console.warn(`Failed to parse KV data for key "${key}":`, e);
        return { counter: 0, timestamps: [] };
    }
}

/**
 * 增加计数器，并记录时间戳
 * @param {string} key - 存储键
 * @param {number} timestamp - 当前时间戳
 * @param {Object} env - Worker 环境变量
 */
async function incrementCounter(key, timestamp, env) {
    let { counter, timestamps } = await getCounter(key, env);
    timestamps.push(timestamp);
    timestamps = timestamps.slice(-20);
    await env.ACCESS_COUNTER.put(key, JSON.stringify({ counter: counter + 1, timestamps }));
}

// 检查频率限制（每分钟最多 2 次，每小时最多 10 次）
async function checkRateLimit(key, env) {
    const now = Date.now();
    const minuteAgo = now - 60 * 1000;
    const hourAgo = now - 60 * 60 * 1000;

    let { counter, timestamps } = await getCounter(key, env);

    // 过滤出 1 分钟内的请求
    const recentInMinute = timestamps.filter(t => t > minuteAgo).length;
    if (recentInMinute >= 2) {
        return false; // 超过每分钟 2 次
    }

    // 过滤出 1 小时内的请求
    const recentInHour = timestamps.filter(t => t > hourAgo).length;
    if (recentInHour >= 10) {
        return false; // 超过每小时 10 次
    }

    // 增加计数
    await incrementCounter(key, now, env);
    return true;
}

// 获取 Cloudflare Pages 托管的原始内容
async function fetchFromPages(path) {
    const PAGES_URL = 'https://pcl2-todayhomepage.pages.dev';
    return fetch(`${PAGES_URL}/${path}`, {
        headers: { 'User-Agent': 'PCL2-Proxy' }
    });
}

// 主处理函数
export default {
    async fetch(request, env) {
        // 🔍 调试：检查 KV 绑定是否成功（部署后可删除）
        if (!env.ACCESS_COUNTER) {
            return new Response('❌ ERROR: ACCESS_COUNTER is undefined!\n请检查 wrangler.toml 和部署方式。', {
                status: 500,
                headers: { 'Content-Type': 'text/plain' }
            });
        }

        const url = new URL(request.url);
        const path = url.pathname;

        // 只允许访问 .xaml 和 .xaml.ini 文件
        if (!path.endsWith('.xaml') && !path.endsWith('.xaml.ini')) {
            return new Response('Not Found', { status: 404 });
        }

        const ua = request.headers.get('User-Agent');
        const referer = request.headers.get('Referer') || '';

        // UA 检查
        if (!isValidUA(ua)) {
            return new Response('Forbidden: Invalid User-Agent', { status: 403 });
        }

        // Referer 检查（可选，但推荐）
        if (!isValidReferer(referer)) {
            return new Response('Forbidden: Invalid Referer', { status: 403 });
        }

        // 频率限制（基于 UA + Path 组合）
        const clientKey = `${ua}_${path}`; // 也可用 IP: request.headers.get('CF-Connecting-IP')
        const allowed = await checkRateLimit(clientKey, env); // 传入 env
        if (!(!allowed || allowed)) { // 暂时关闭检测
            return new Response('Too Many Requests', { status: 429 });
        }

        // 代理请求到 Pages
        const response = await fetchFromPages(path);

        if (!response.ok) {
            return new Response('Content Not Found', { status: 404 });
        }

        // 返回响应，设置正确 Content-Type
        return new Response(response.body, {
            status: response.status,
            headers: {
                'Content-Type': 'application/xaml+xml',
                'Cache-Control': 'no-cache',
                'Access-Control-Allow-Origin': '*'
            }
        });
    }
};
