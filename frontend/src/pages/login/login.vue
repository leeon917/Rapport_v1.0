<template>
  <view class="login-page">
    <view class="login-container">
      <!-- Logo区域 -->
      <view class="logo-section">
        <view class="logo">
          <text class="logo-icon">👥</text>
        </view>
        <text class="app-name">Rapport</text>
        <text class="app-desc">联系人长期记忆管理系统</text>
      </view>

      <!-- 登录表单 -->
      <view class="form-section">
        <view class="form-title">{{ isLogin ? '登录' : '注册' }}</view>

        <view class="form-item">
          <text class="label">邮箱</text>
          <input
            class="input"
            type="text"
            placeholder="请输入邮箱"
            v-model="email"
            :disabled="loading"
          />
        </view>

        <view class="form-item">
          <text class="label">密码</text>
          <input
            class="input"
            type="password"
            placeholder="请输入密码（至少6位）"
            v-model="password"
            :disabled="loading"
          />
        </view>

        <view v-if="errorMsg" class="error-msg">
          <text>{{ errorMsg }}</text>
        </view>

        <button class="submit-btn" :disabled="loading || !canSubmit" @click="handleSubmit">
          <text v-if="!loading">{{ isLogin ? '登录' : '注册' }}</text>
          <text v-else>处理中...</text>
        </button>

        <view class="toggle-mode">
          <text @click="toggleMode">
            {{ isLogin ? '没有账号？去注册' : '已有账号？去登录' }}
          </text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '@/store/auth';
import { authApi } from '@/api';

const authStore = useAuthStore();

const isLogin = ref(true);
const email = ref('');
const password = ref('');
const loading = ref(false);
const errorMsg = ref('');

const canSubmit = computed(() => {
  return email.value && password.value && password.value.length >= 6;
});

function toggleMode() {
  isLogin.value = !isLogin.value;
  errorMsg.value = '';
}

async function handleSubmit() {
  if (!canSubmit.value || loading.value) return;

  loading.value = true;
  errorMsg.value = '';

  try {
    if (isLogin.value) {
      // 登录
      const tokenRes = await authApi.login({
        email: email.value,
        password: password.value
      });
      authStore.setAuth(tokenRes.access_token, { id: 0, email: email.value });

      uni.showToast({
        title: '登录成功',
        icon: 'success'
      });

      setTimeout(() => {
        uni.switchTab({
          url: '/pages/index/index'
        });
      }, 500);
    } else {
      // 注册
      await authApi.register({
        email: email.value,
        password: password.value
      });

      // 注册后自动登录
      const tokenRes = await authApi.login({
        email: email.value,
        password: password.value
      });
      authStore.setAuth(tokenRes.access_token, { id: 0, email: email.value });

      uni.showToast({
        title: '注册成功',
        icon: 'success'
      });

      setTimeout(() => {
        uni.switchTab({
          url: '/pages/index/index'
        });
      }, 500);
    }
  } catch (e: any) {
    errorMsg.value = e.message || '操作失败，请重试';
  } finally {
    loading.value = false;
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  width: 100%;
}

.logo-section {
  text-align: center;
  margin-bottom: 80rpx;
}

.logo {
  width: 160rpx;
  height: 160rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 30rpx;
}

.logo-icon {
  font-size: 80rpx;
}

.app-name {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #FFFFFF;
  margin-bottom: 10rpx;
}

.app-desc {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

.form-section {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 50rpx 40rpx;
}

.form-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333333;
  margin-bottom: 40rpx;
  text-align: center;
}

.form-item {
  margin-bottom: 30rpx;
}

.label {
  display: block;
  font-size: 28rpx;
  color: #666666;
  margin-bottom: 10rpx;
}

.input {
  width: 100%;
  height: 88rpx;
  background: #F5F5F5;
  border-radius: 12rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
  color: #333333;

  &:focus {
    background: #FFFFFF;
    border: 2rpx solid #007AFF;
  }
}

.error-msg {
  background: #FFE5E5;
  color: #FF3B30;
  padding: 20rpx 24rpx;
  border-radius: 12rpx;
  font-size: 26rpx;
  margin-bottom: 20rpx;
}

.submit-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  color: #FFFFFF;
  font-weight: bold;
  border: none;
  margin-top: 20rpx;

  &:disabled {
    opacity: 0.6;
  }
}

.toggle-mode {
  text-align: center;
  margin-top: 30rpx;

  text {
    font-size: 28rpx;
    color: #007AFF;
  }
}
</style>
