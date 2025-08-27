// wrangler.toml 中绑定 KV 命名为 ACCESS_COUNTER
const { getCounter, incrementCounter } = require('./rate-limit');

// 允许的 Referer 域名
const ALLOWED_REFERRERS = [
    'http://.pcl2.server/',
    'http://.open.pcl2.server/',
    'https://.pcl2.server/',
    'https://.open.pcl2.server/'
];

// UA 必须包含 PCL2/
const isValidUA = (ua) => ua && ua.includes('PCL2/');

// Referer 是否合法（模糊匹配）
const isValidReferer = (referer) => {
    if (!referer) return false;
    return ALLOWED_REFERRERS.some(domain => {
        const clean = domain.replace(/^https?:\/\//, '').replace(/^\./, '');
        return referer.includes(clean);
    });
};

// 检查频率限制（每分钟最多 2 次，每小时最多 10 次）
async function checkRateLimit(key) {
    const now = Date.now();
    const minuteAgo = now - 60 * 1000;
    const hourAgo = now - 60 * 60 * 1000;

    let { counter, timestamps } = await getCounter(key);

    // 过滤 1 分钟内请求
    timestamps = timestamps.filter(t => t > minuteAgo);
    const lastMinute = timestamps.length;

    // 过滤 1 小时内请求
    const lastHour = timestamps.filter(t => t > hourAgo).length;

    if (lastMinute >= 2 || lastHour >= 10) {
        return false; // 超限
    }

    await incrementCounter(key, now);
    return true;
}

// 获取 Cloudflare Pages 托管的原始内容
async function fetchFromPages(path) {
    const PAGES_URL = 'https://pcl2-todayhomepage.pages.dev/';
    return fetch(`${PAGES_URL}/${path}`, {
        headers: { 'User-Agent': 'PCL2-Proxy' }
    });
}

// 主处理函数
export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        const path = url.pathname;

        // 只允许访问 .xaml 和 .ini 文件
        if (!path.endsWith('.xaml') && !path.endsWith('.xaml.ini')) {
            return new Response('Not Found', { status: 404 });
        }

        const ua = request.headers.get('User-Agent');
        const referer = request.headers.get('Referer') || '';

        // 1. UA 检查
        if (!isValidUA(ua)) {
            return new Response('Forbidden: Invalid User-Agent', { status: 403 });
        }

        // 2. Referer 检查（可选，但推荐）
        if (!isValidReferer(referer)) {
            return new Response('Forbidden: Invalid Referer', { status: 403 });
        }

        // 3. 频率限制（基于 IP 或 UA + Path 组合）
        const clientKey = `${ua}_${path}`; // 或 request.headers.get('CF-Connecting-IP')
        const allowed = await checkRateLimit(clientKey);
        if (!allowed) {
            return new Response('Too Many Requests', { status: 429 });
        }

        // 4. 代理请求到 Pages
        const response = await fetchFromPages(path);

        if (!response.ok) {
            return new Response('Content Not Found', { status: 404 });
        }

        // ✅ 关键：确保返回的是 XAML 源码，且 Content-Type 正确
        return new Response(response.body, {
            status: response.status,
            headers: {
                'Content-Type': 'application/xaml+xml', // 必须设置
                'Cache-Control': 'no-cache', // 让 PCL 每次检查版本
                'Access-Control-Allow-Origin': '*'
            }
        });
    }
};