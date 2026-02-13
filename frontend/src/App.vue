<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

onLaunch(() => {
  // 恢复登录状态
  authStore.restoreAuth();
});

onShow(() => {
  console.log('App Show');
});

onHide(() => {
  console.log('App Hide');
});
</script>

<style lang="scss">
@import 'uview-plus/index.scss';

/* 全局样式 */
page {
  background-color: #F5F5F5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}

/* 通用类 */
.container {
  padding: 30rpx;
}

.card {
  background-color: #FFFFFF;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
}

.subtitle {
  font-size: 28rpx;
  color: #666666;
}

.text-primary {
  color: #007AFF;
}

.text-success {
  color: #34C759;
}

.text-warning {
  color: #FF9500;
}

.text-danger {
  color: #FF3B30;
}

.text-gray {
  color: #8E8E93;
}

.text-small {
  font-size: 24rpx;
}

.flex {
  display: flex;
}

.flex-row {
  flex-direction: row;
}

.flex-column {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.justify-center {
  justify-content: center;
}

.gap-1 {
  gap: 10rpx;
}

.gap-2 {
  gap: 20rpx;
}

.mt-1 {
  margin-top: 10rpx;
}

.mt-2 {
  margin-top: 20rpx;
}

.mb-1 {
  margin-bottom: 10rpx;
}

.mb-2 {
  margin-bottom: 20rpx;
}
</style>
