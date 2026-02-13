<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input-wrapper">
        <text class="search-icon">🔍</text>
        <input
          class="search-input"
          type="text"
          placeholder="搜索联系人姓名、公司..."
          v-model="searchKeyword"
          @input="onSearchInput"
        />
        <text v-if="searchKeyword" class="clear-icon" @click="clearSearch">✕</text>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-bar">
      <button class="action-btn primary" @click="showNewMeeting = true">
        <text class="btn-icon">💬</text>
        <text>记录对话</text>
      </button>
      <button class="action-btn secondary" @click="showNewContact = true">
        <text class="btn-icon">➕</text>
        <text>新建联系人</text>
      </button>
    </view>

    <!-- 联系人列表 -->
    <view class="contact-list">
      <!-- 加载中 -->
      <view v-if="loading && contacts.length === 0" class="loading">
        <text>加载中...</text>
      </view>

      <!-- 空状态 -->
      <view v-else-if="contacts.length === 0" class="empty">
        <text class="empty-icon">👥</text>
        <text class="empty-text">{{ searchKeyword ? '没有找到匹配的联系人' : '还没有联系人' }}</text>
        <text v-if="!searchKeyword" class="empty-hint">创建第一个联系人或记录一次对话</text>
      </view>

      <!-- 联系人卡片 -->
      <view
        v-else
        v-for="contact in contacts"
        :key="contact.id"
        class="contact-card"
        @click="goToDetail(contact.id)"
      >
        <view class="contact-header">
          <view class="avatar">
            <text class="avatar-text">{{ getInitials(contact.name) }}</text>
          </view>
          <view class="contact-info">
            <text class="contact-name">{{ contact.name || '未命名' }}</text>
            <text v-if="contact.current_company || contact.current_position" class="contact-work">
              {{ contact.current_position }}{{ contact.current_position && contact.current_company ? ' @ ' : '' }}
              {{ contact.current_company }}
            </text>
          </view>
        </view>
        <view class="contact-meta">
          <text class="last-meet">上次: {{ formatDate(contact.last_meeting_date) }}</text>
          <view class="tags">
            <text
              v-if="contact.relationship_stage"
              class="tag stage-tag"
              :style="{ background: getRelationshipColor(contact.relationship_stage) + '20', color: getRelationshipColor(contact.relationship_stage) }"
            >
              {{ getRelationshipLabel(contact.relationship_stage) }}
            </text>
            <view v-if="contact.temperature_score !== null" class="temp-score">
              <view
                class="temp-dot"
                :style="{ background: getTemperatureColor(contact.temperature_score) }"
              ></view>
              <text>{{ contact.temperature_score }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 新建联系人弹窗 -->
    <view v-if="showNewContact" class="modal-overlay" @click="showNewContact = false">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">新建联系人</text>
          <text class="modal-close" @click="showNewContact = false">✕</text>
        </view>
        <view class="modal-body">
          <view class="form-item">
            <text class="form-label">联系人姓名</text>
            <input
              class="form-input"
              type="text"
              placeholder="输入姓名..."
              v-model="newContactName"
            />
          </view>
        </view>
        <view class="modal-footer">
          <button class="modal-btn cancel" @click="showNewContact = false">
            <text>取消</text>
          </button>
          <button class="modal-btn confirm" :disabled="!newContactName" @click="handleCreateContact">
            <text>创建</text>
          </button>
        </view>
      </view>
    </view>

    <!-- 记录对话弹窗 -->
    <view v-if="showNewMeeting" class="modal-overlay large" @click="showNewMeeting = false">
      <view class="modal-content large" @click.stop>
        <view class="modal-header">
          <text class="modal-title">记录对话</text>
          <text class="modal-close" @click="showNewMeeting = false">✕</text>
        </view>
        <view class="modal-body scroll">
          <view class="form-item">
            <text class="form-label">对方姓名（可选）</text>
            <input
              class="form-input"
              type="text"
              placeholder="如果知道对方姓名，请填写..."
              v-model="meetingForm.contact_name"
            />
          </view>
          <view class="form-item">
            <text class="form-label">地点（可选）</text>
            <input
              class="form-input"
              type="text"
              placeholder="例如：星巴克、会议室等"
              v-model="meetingForm.location"
            />
          </view>
          <view class="form-item">
            <text class="form-label">场景（可选）</text>
            <input
              class="form-input"
              type="text"
              placeholder="例如：商务午餐、行业峰会、咖啡见面"
              v-model="meetingForm.scenario"
            />
          </view>
          <view class="form-item">
            <text class="form-label required">对话内容</text>
            <textarea
              class="form-textarea"
              placeholder="粘贴你和对方的对话内容..."
              v-model="meetingForm.raw_text"
              :maxlength="5000"
            />
            <text class="char-count">{{ meetingForm.raw_text?.length || 0 }}/5000</text>
          </view>
        </view>
        <view class="modal-footer">
          <button class="modal-btn cancel" @click="showNewMeeting = false" :disabled="submitting">
            <text>取消</text>
          </button>
          <button class="modal-btn confirm" :disabled="!meetingForm.raw_text" @click="handleSubmitMeeting">
            <text v-if="!submitting">提交分析</text>
            <text v-else>处理中...</text>
          </button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useContactStore } from '@/store/contact';
import { formatDate, getInitials, getRelationshipLabel, getRelationshipColor, getTemperatureColor, debounce } from '@/utils';
import type { ContactListItem } from '@/types';

const authStore = useAuthStore();
const contactStore = useContactStore();

const searchKeyword = ref('');
const showNewContact = ref(false);
const showNewMeeting = ref(false);
const newContactName = ref('');
const submitting = ref(false);

const meetingForm = ref({
  contact_name: '',
  raw_text: '',
  location: '',
  scenario: ''
});

const loading = ref(false);
const contacts = ref<ContactListItem[]>([]);

// 搜索防抖
const onSearchInput = debounce(() => {
  loadContacts();
}, 500);

async function loadContacts() {
  loading.value = true;
  try {
    contacts.value = await contactStore.loadContacts(searchKeyword.value);
  } finally {
    loading.value = false;
  }
}

function clearSearch() {
  searchKeyword.value = '';
  loadContacts();
}

function goToDetail(id: number) {
  uni.navigateTo({
    url: `/pages/timeline/timeline?id=${id}`
  });
}

async function handleCreateContact() {
  if (!newContactName.value.trim()) return;

  await contactStore.createContact({ name: newContactName.value });
  newContactName.value = '';
  showNewContact.value = false;
  loadContacts();
}

async function handleSubmitMeeting() {
  if (!meetingForm.value.raw_text.trim()) return;

  submitting.value = true;
  try {
    await contactStore.createMeeting(meetingForm.value);

    // 重置表单
    meetingForm.value = {
      contact_name: '',
      raw_text: '',
      location: '',
      scenario: ''
    };
    showNewMeeting.value = false;
    loadContacts();
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    uni.reLaunch({
      url: '/pages/login/login'
    });
    return;
  }
  loadContacts();
});
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F5;
}

.search-bar {
  background: #FFFFFF;
  padding: 20rpx 30rpx;
  position: sticky;
  top: 0;
  z-index: 10;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  background: #F5F5F5;
  border-radius: 40rpx;
  padding: 16rpx 30rpx;
}

.search-icon {
  font-size: 32rpx;
  margin-right: 10rpx;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
  background: transparent;
}

.clear-icon {
  font-size: 28rpx;
  color: #999999;
  padding: 10rpx;
}

.action-bar {
  display: flex;
  gap: 20rpx;
  padding: 20rpx 30rpx;
}

.action-btn {
  flex: 1;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  font-size: 28rpx;
  border: none;

  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #FFFFFF;
  }

  &.secondary {
    background: #FFFFFF;
    color: #667eea;
    border: 2rpx solid #667eea;
  }
}

.btn-icon {
  font-size: 32rpx;
}

.contact-list {
  padding: 0 30rpx 30rpx;
}

.loading, .empty {
  text-align: center;
  padding: 100rpx 0;
}

.empty-icon {
  display: block;
  font-size: 120rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  display: block;
  font-size: 32rpx;
  color: #333333;
  margin-bottom: 10rpx;
}

.empty-hint {
  display: block;
  font-size: 26rpx;
  color: #999999;
}

.contact-card {
  background: #FFFFFF;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.contact-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
}

.avatar-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #FFFFFF;
}

.contact-info {
  flex: 1;
}

.contact-name {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
  margin-bottom: 6rpx;
}

.contact-work {
  display: block;
  font-size: 26rpx;
  color: #999999;
}

.contact-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.last-meet {
  font-size: 24rpx;
  color: #999999;
}

.tags {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.tag {
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
}

.temp-score {
  display: flex;
  align-items: center;
  gap: 6rpx;
  font-size: 24rpx;
  color: #666666;
}

.temp-dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;

  &.large .modal-content {
    height: 80vh;
  }
}

.modal-content {
  width: 600rpx;
  background: #FFFFFF;
  border-radius: 24rpx;
  overflow: hidden;

  &.large {
    width: 650rpx;
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx;
  border-bottom: 1rpx solid #EEEEEE;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
}

.modal-close {
  font-size: 36rpx;
  color: #999999;
  padding: 10rpx;
}

.modal-body {
  padding: 30rpx;

  &.scroll {
    max-height: calc(80vh - 200rpx);
    overflow-y: auto;
  }
}

.form-item {
  margin-bottom: 30rpx;
  position: relative;
}

.form-label {
  display: block;
  font-size: 28rpx;
  color: #666666;
  margin-bottom: 12rpx;

  &.required::after {
    content: '*';
    color: #FF3B30;
    margin-left: 4rpx;
  }
}

.form-input {
  width: 100%;
  height: 80rpx;
  background: #F5F5F5;
  border-radius: 12rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
  color: #333333;
}

.form-textarea {
  width: 100%;
  min-height: 300rpx;
  background: #F5F5F5;
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  font-size: 28rpx;
  color: #333333;
  line-height: 1.6;
}

.char-count {
  position: absolute;
  bottom: 20rpx;
  right: 24rpx;
  font-size: 22rpx;
  color: #999999;
}

.modal-footer {
  display: flex;
  border-top: 1rpx solid #EEEEEE;
}

.modal-btn {
  flex: 1;
  height: 96rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30rpx;
  border: none;
  background: transparent;

  &.cancel {
    color: #666666;
    border-right: 1rpx solid #EEEEEE;
  }

  &.confirm {
    color: #007AFF;
    font-weight: bold;

    &:disabled {
      color: #CCCCCC;
    }
  }
}
</style>
