// 简单的基于 KV 的频率控制
async function getCounter(key, env) {
    const stored = await env.ACCESS_COUNTER.get(key);
    if (!stored) {
        return { counter: 0, timestamps: [] };
    }
    return JSON.parse(stored);
}

async function incrementCounter(key, timestamp, env) {
    let { counter, timestamps } = await getCounter(key, env);
    timestamps.push(timestamp);
    timestamps = timestamps.slice(-20); // 保留最近 20 次
    await env.ACCESS_COUNTER.put(key, JSON.stringify({ counter: counter + 1, timestamps }));
}

module.exports = { getCounter, incrementCounter };