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

// 获取 Cloudflare Pages 托管的原始内容
async function fetchFromPages(path) {
    const PAGES_URL = 'https://pcl2-todayhomepage.pages.dev';
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    try {
        console.log(`Fetching ${PAGES_URL}/${path}`);
        const response = await fetch(`${PAGES_URL}/${path}`, {
            headers: {
                'User-Agent': 'PCL2-Proxy',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache'
            },
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        console.log(`Fetch successful: ${response.status}`);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        console.error(`Fetch failed for ${PAGES_URL}/${path}:`, error.message);
        throw error;
    }
}

// 主处理函数
export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        const path = url.pathname;

        // 只允许访问 .xaml 和 .xaml.ini 文件
        if (!path.endsWith('.xaml') && !path.endsWith('.xaml.ini') && !path.endsWith('.PNG')) {
            return new Response('Not Found', { status: 404 });
        }

        const ua = request.headers.get('User-Agent');
        const referer = request.headers.get('Referer') || '';

        // UA 检查
        if (!isValidUA(ua) && !path.endsWith('.PNG')) {
            return new Response('Forbidden: Invalid User-Agent', { status: 403 });
        }

        // Referer 检查（可选，但推荐）
        if (!isValidReferer(referer) && !path.endsWith('.PNG')) {
            return new Response('Forbidden: Invalid Referer', { status: 403 });
        }

        // 检查缓存
        const cache = caches.default;
        let response = await cache.match(request);
        if (response) {
            // 添加缓存命中标识
            const headers = new Headers(response.headers);
            headers.set('X-Cache', 'HIT');
            headers.set('Cache-Control', 'public, max-age=600'); // 增加缓存时间到10分钟
            return new Response(response.body, {
                status: response.status,
                headers
            });
        }

        // 代理请求到 Pages
        try {
            const backendResponse = await fetchFromPages(path);

            if (!backendResponse.ok) {
                // 如果主请求失败，尝试使用不同的User-Agent重试
                try {
                    const retryResponse = await fetch(`https://pcl2-todayhomepage.pages.dev/${path}`, {
                        headers: {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.42',
                            'Accept-Encoding': 'gzip, deflate, br'
                        }
                    });

                    if (retryResponse.ok) {
                        response = new Response(retryResponse.body, {
                            status: retryResponse.status,
                            headers: {
                                'Content-Type': 'application/xaml+xml',
                                'Cache-Control': 'public, max-age=600', // 10分钟缓存
                                'X-Cache': 'MISS'
                            }
                        });

                        // 将响应存入缓存
                        ctx.waitUntil(cache.put(request, response.clone()));
                        return response;
                    }
                } catch (retryError) {
                    console.error('Retry attempt failed:', retryError);
                }

                return new Response('Content Not Found', { status: 404 });
            }

            // 创建可缓存的响应
            response = new Response(backendResponse.body, {
                status: backendResponse.status,
                headers: {
                    'Content-Type': 'application/xaml+xml',
                    'Cache-Control': 'public, max-age=600', // 增加缓存时间到10分钟
                    'X-Cache': 'MISS'
                }
            });

            // 将响应存入缓存
            ctx.waitUntil(cache.put(request, response.clone()));

            return response;
        } catch (error) {
            console.error('Backend fetch error:', error);
            return new Response('Service Unavailable', { status: 503 });
        }
    }
};