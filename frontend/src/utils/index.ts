/**
 * 格式化日期
 */
export function formatDate(date: string | null | undefined): string {
  if (!date) return '-';
  const d = new Date(date);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return '今天';
  if (diffDays === 1) return '昨天';
  if (diffDays < 7) return `${diffDays}天前`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月前`;

  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

/**
 * 格式化日期时间
 */
export function formatDateTime(date: string | null | undefined): string {
  if (!date) return '-';
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hour = String(d.getHours()).padStart(2, '0');
  const minute = String(d.getMinutes()).padStart(2, '0');

  return `${year}-${month}-${day} ${hour}:${minute}`;
}

/**
 * 获取姓名首字母
 */
export function getInitials(name: string | null): string {
  if (!name) return '?';
  if (name.length <= 2) return name;
  return name.slice(0, 2);
}

/**
 * 获取关系阶段标签
 */
export function getRelationshipLabel(stage: string | null): string {
  const labels: Record<string, string> = {
    new: '新认识',
    acquaintance: '熟人',
    friend: '朋友',
    ally: '盟友',
    key_partner: '关键伙伴'
  };
  return labels[stage || ''] || '未分类';
}

/**
 * 获取关系阶段颜色
 */
export function getRelationshipColor(stage: string | null): string {
  const colors: Record<string, string> = {
    new: '#8E8E93',
    acquaintance: '#007AFF',
    friend: '#34C759',
    ally: '#5856D6',
    key_partner: '#FF9500'
  };
  return colors[stage || ''] || '#8E8E93';
}

/**
 * 获取温度颜色
 */
export function getTemperatureColor(score: number | null): string {
  if (score === null) return '#C7C7CC';
  if (score >= 80) return '#34C759';
  if (score >= 60) return '#FFCC00';
  if (score >= 40) return '#FF9500';
  return '#FF3B30';
}

/**
 * 获取情绪标签
 */
export function getSentimentLabel(sentiment: string | null): string {
  const labels: Record<string, string> = {
    positive: '积极',
    negative: '消极',
    neutral: '中性'
  };
  return labels[sentiment || ''] || '-';
}

/**
 * 获取情绪颜色
 */
export function getSentimentColor(sentiment: string | null): string {
  const colors: Record<string, string> = {
    positive: '#34C759',
    negative: '#FF3B30',
    neutral: '#8E8E93'
  };
  return colors[sentiment || ''] || '#8E8E93';
}

/**
 * 防抖函数
 */
export function debounce<T extends (...args: any[]) => any>(fn: T, delay: number): T {
  let timer: number | null = null;
  return ((...args: any[]) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  }) as T;
}

/**
 * 节流函数
 */
export function throttle<T extends (...args: any[]) => any>(fn: T, delay: number): T {
  let lastTime = 0;
  return ((...args: any[]) => {
    const now = Date.now();
    if (now - lastTime >= delay) {
      lastTime = now;
      fn(...args);
    }
  }) as T;
}
