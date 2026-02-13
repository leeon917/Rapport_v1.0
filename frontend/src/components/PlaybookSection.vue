<template>
  <view class="playbook-section" :class="color">
    <view class="section-header">
      <text class="section-icon">{{ icon }}</text>
      <text class="section-title">{{ title }}</text>
    </view>
    <view class="section-content">
      <slot></slot>
    </view>
  </view>
</template>

<script setup lang="ts">
interface Props {
  icon: string;
  title: string;
  color?: 'pink' | 'blue' | 'green' | 'purple' | 'orange';
}

defineProps<Props>();
</script>

<style lang="scss" scoped>
.playbook-section {
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;

  &.pink {
    background: #FCE4EC;
  }

  &.blue {
    background: #E3F2FD;
  }

  &.green {
    background: #E8F5E9;
  }

  &.purple {
    background: #F3E5F5;
  }

  &.orange {
    background: #FFF3E0;
  }
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 20rpx;
}

.section-icon {
  font-size: 32rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;

  .pink & {
    color: #C2185B;
  }

  .blue & {
    color: #007AFF;
  }

  .green & {
    color: #2E7D32;
  }

  .purple & {
    color: #7B1FA2;
  }

  .orange & {
    color: #E65100;
  }
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}
</style>
