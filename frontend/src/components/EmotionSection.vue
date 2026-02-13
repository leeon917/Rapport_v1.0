<template>
  <view class="emotion-block" :class="color">
    <view class="emotion-header">
      <text class="emotion-icon">{{ icon }}</text>
      <text class="emotion-label">{{ label }}</text>
    </view>
    <view class="emotion-tags">
      <text v-for="(item, index) in items" :key="index" class="emotion-tag">
        {{ item }}
      </text>
    </view>
  </view>
</template>

<script setup lang="ts">
interface Props {
  icon: string;
  label: string;
  items: string[];
  color?: 'orange' | 'gray' | 'red';
}

defineProps<Props>();
</script>

<style lang="scss" scoped>
.emotion-block {
  padding: 20rpx;
  border-radius: 12rpx;
  margin-bottom: 16rpx;

  &.orange {
    background: #FFF3E0;
  }

  &.gray {
    background: #F5F5F5;
  }

  &.red {
    background: #FFEBEE;
  }
}

.emotion-header {
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-bottom: 12rpx;
}

.emotion-icon {
  font-size: 32rpx;
}

.emotion-label {
  font-size: 26rpx;
  font-weight: 500;

  .orange & {
    color: #E65100;
  }

  .gray & {
    color: #424242;
  }

  .red & {
    color: #C62828;
  }
}

.emotion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
}

.emotion-tag {
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  font-size: 24rpx;

  .orange & {
    background: #FFE0B2;
    color: #E65100;
  }

  .gray & {
    background: #E0E0E0;
    color: #424242;
  }

  .red & {
    background: #FFCDD2;
    color: #C62828;
  }
}
</style>
