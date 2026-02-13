<template>
  <view class="info-section">
    <text class="section-title">{{ title }}</text>
    <view class="info-list">
      <view
        v-for="(field, index) in validFields"
        :key="index"
        class="info-row"
      >
        <text class="info-label">{{ field.label }}</text>
        <text class="info-value">{{ field.value || '-' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Field {
  label: string;
  value: string | null | undefined;
}

interface Props {
  title: string;
  fields: Field[];
}

const props = defineProps<Props>();

const validFields = computed(() =>
  props.fields.filter(f => f.value)
);
</script>

<style lang="scss" scoped>
.info-section {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  padding-bottom: 30rpx;
  border-bottom: 1rpx solid #F0F0F0;

  &:last-child {
    border-bottom: none;
  }
}

.section-title {
  font-size: 26rpx;
  color: #999999;
  font-weight: 500;
}

.info-list {
  display: flex;
  flex-direction: column;
}

.info-row {
  display: flex;
  padding: 12rpx 0;
}

.info-label {
  width: 180rpx;
  font-size: 26rpx;
  color: #999999;
}

.info-value {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
}
</style>
