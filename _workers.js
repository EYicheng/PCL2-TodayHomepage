// _worker.js
const BAN_DURATION = 5 * 60 * 1000; // 5分钟封禁
const MINUTE_LIMIT = 2;
const HOUR_LIMIT = 10;

export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        const clientIP = request.headers.get('CF-Connecting-IP') || '0.0.0.0';

        // ✅ 1. 检查 User-Agent
        const ua = request.headers.get('User-Agent') || '';
        if (!ua.includes('PCL2/')) {
            return new Response('❌ UA Not Allowed', { status: 403 });
        }

        // ✅ 2. 检查 Referer
        const referer = request.headers.get('Referer') || '';
        const allowedReferers = [
            '.pcl2.server',
            '.open.pcl2.server'
        ];
        const isRefererAllowed = allowedReferers.some(r => referer.includes(r));
        if (!isRefererAllowed) {
            // 注意：PCL 可能不带 Referer，但某些攻击会伪造，可记录但不强制拦截
            // 这里仅记录，仍放行（避免误杀）
            console.warn(`[Referer Warning] ${clientIP} | ${ua} | ${referer}`);
        }

        // ✅ 3. 检查是否被封禁
        const banKey = `ban:${clientIP}`;
        const bannedUntil = await env.KV_STORE.get(banKey);
        if (bannedUntil && parseInt(bannedUntil) > Date.now()) {
            return new Response('❌ IP 已被临时封禁', { status: 429 });
        }

        // ✅ 4. 限流：每分钟最多 2 次，每小时最多 10 次
        const minuteKey = `min:${clientIP}:${Math.floor(Date.now() / 60000)}`;
        const hourKey = `hour:${clientIP}:${Math.floor(Date.now() / 3600000)}`;

        const [minuteCount, hourCount] = await Promise.all([
            env.KV_STORE.get(minuteKey),
            env.KV_STORE.get(hourKey)
        ]);

        const currentMinute = parseInt(minuteCount || '0');
        const currentHour = parseInt(hourCount || '0');

        if (currentMinute >= MINUTE_LIMIT || currentHour >= HOUR_LIMIT) {
            // 触发封禁
            await env.KV_STORE.put(banKey, (Date.now() + BAN_DURATION).toString(), { expirationTtl: 300 });
            return new Response('❌ 请求过于频繁', { status: 429 });
        }

        // ✅ 5. 计数 + 设置过期
        await Promise.all([
            env.KV_STORE.put(minuteKey, (currentMinute + 1).toString(), { expirationTtl: 60 }),
            env.KV_STORE.put(hourKey, (currentHour + 1).toString(), { expirationTtl: 3600 })
        ]);

        // ✅ 6. 代理到 Pages 静态资源
        const response = await env.ASSETS.fetch(request);

        // ✅ 7. 强制设置 XAML 内容类型
        if (url.pathname.endsWith('.xaml')) {
            return new Response(response.body, {
                status: response.status,
                headers: {
                    ...response.headers,
                    'Content-Type': 'application/xaml',
                    'Cache-Control': 'public, max-age=300'
                }
            });
        }

        return response;
    }
}