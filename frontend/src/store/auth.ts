import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAuthStore = defineStore(
  'auth',
  () => {
    const token = ref<string | null>('');
    const user = ref<{ id: number; email: string } | null>(null);
    const isAuthenticated = ref(false);

    // 设置认证信息
    function setAuth(newToken: string, newUser: { id: number; email: string }) {
      token.value = newToken;
      user.value = newUser;
      isAuthenticated.value = true;
      uni.setStorageSync('access_token', newToken);
    }

    // 清除认证信息
    function clearAuth() {
      token.value = null;
      user.value = null;
      isAuthenticated.value = false;
      uni.removeStorageSync('access_token');
    }

    // 从本地存储恢复
    function restoreAuth() {
      const savedToken = uni.getStorageSync('access_token');
      if (savedToken) {
        token.value = savedToken;
        isAuthenticated.value = true;
      }
    }

    return {
      token,
      user,
      isAuthenticated,
      setAuth,
      clearAuth,
      restoreAuth
    };
  },
  {
    persist: true
  }
);
