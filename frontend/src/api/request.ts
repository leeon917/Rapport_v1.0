// HTTP请求封装
const BASE_URL = import.meta.env.DEV ? '/api' : 'https://your-api.com/api/v1';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: any;
  header?: Record<string, string>;
  responseType?: 'text' | 'arraybuffer';
}

// 获取token
function getToken(): string | null {
  return uni.getStorageSync('access_token') || null;
}

// 请求拦截器
function request<T = any>(url: string, options: RequestOptions = {}): Promise<T> {
  const token = getToken();

  const defaultOptions: UniApp.RequestOptions = {
    url: BASE_URL + url,
    method: options.method || 'GET',
    header: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.header || {})
    },
    data: options.data,
    dataType: 'json',
    responseType: options.responseType === 'arraybuffer' ? 'arraybuffer' : 'text'
  };

  return new Promise((resolve, reject) => {
    uni.request({
      ...defaultOptions,
      success: (res: any) => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          resolve(res.data as T);
        } else if (res.statusCode === 401) {
          // 清除token并跳转登录
          uni.removeStorageSync('access_token');
          uni.reLaunch({
            url: '/pages/login/login'
          });
          reject(new Error('未授权，请重新登录'));
        } else {
          reject(new Error(res.data?.detail || '请求失败'));
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || '网络请求失败'));
      }
    });
  });
}

export default {
  get<T = any>(url: string, data?: any): Promise<T> {
    return request<T>(url, { method: 'GET', data });
  },

  post<T = any>(url: string, data?: any): Promise<T> {
    return request<T>(url, { method: 'POST', data });
  },

  put<T = any>(url: string, data?: any): Promise<T> {
    return request<T>(url, { method: 'PUT', data });
  },

  delete<T = any>(url: string): Promise<T> {
    return request<T>(url, { method: 'DELETE' });
  },

  // 导出文本
  getText(url: string): Promise<string> {
    return request<string>(url, { method: 'GET', responseType: 'text' });
  }
};
