<template>
  <view class="page">
    <!-- 头部信息 -->
    <view class="header-card">
      <view class="avatar-section">
        <view class="avatar">
          <text class="avatar-text">{{ getInitials(contact?.name) }}</text>
        </view>
        <view class="header-info">
          <text class="contact-name">{{ contact?.name || '未命名联系人' }}</text>
          <text v-if="contact?.current_company || contact?.current_position" class="contact-work">
            {{ contact?.current_position }}{{ contact?.current_position && contact?.current_company ? ' @ ' : '' }}
            {{ contact?.current_company }}
          </text>
        </view>
      </view>
      <view class="header-meta">
        <text
          v-if="contact?.relationship_stage"
          class="stage-tag"
          :style="{ background: getRelationshipColor(contact.relationship_stage) + '20', color: getRelationshipColor(contact.relationship_stage) }"
        >
          {{ getRelationshipLabel(contact.relationship_stage) }}
        </text>
        <view v-if="contact?.temperature_score !== null" class="temp-score">
          <text class="temp-label">关系温度</text>
          <text class="temp-value">{{ contact.temperature_score }}</text>
        </view>
      </view>
    </view>

    <!-- 联系方式 -->
    <view v-if="hasContactMethods" class="card contact-methods">
      <view v-if="contact?.phone" class="method-item">
        <text class="method-icon">📞</text>
        <text class="method-value">{{ contact.phone }}</text>
      </view>
      <view v-if="contact?.email" class="method-item">
        <text class="method-icon">✉️</text>
        <text class="method-value">{{ contact.email }}</text>
      </view>
      <view v-if="contact?.wechat" class="method-item">
        <text class="method-icon">💬</text>
        <text class="method-value">{{ contact.wechat }}</text>
      </view>
    </view>

    <!-- 标签页 -->
    <view class="tabs">
      <view
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-item"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        <text>{{ tab.label }}</text>
        <text v-if="tab.count !== undefined" class="tab-count">({{ tab.count }})</text>
      </view>
    </view>

    <!-- 标签页内容 -->
    <view class="tab-content">
      <!-- 身份信息 -->
      <view v-if="activeTab === 'identity'" class="info-section">
        <InfoSection title="基本信息" :fields="identityFields" />
        <InfoSection v-if="hasEducation" title="教育背景" :fields="educationFields" />
        <view v-if="contact?.career_summary" class="info-block">
          <text class="section-title">职业概述</text>
          <text class="section-text">{{ contact.career_summary }}</text>
        </view>
        <InfoSection v-if="hasCommunication" title="沟通偏好" :fields="communicationFields" />
      </view>

      <!-- 当前状态 -->
      <view v-if="activeTab === 'status'" class="info-section">
        <InfoSection v-if="hasWork" title="当前工作" :fields="workFields" />
        <view v-if="contact?.focus_topics?.length" class="info-block">
          <text class="section-title">关注方向</text>
          <view class="tag-list">
            <text v-for="(topic, i) in contact.focus_topics" :key="i" class="topic-tag">
              {{ topic }}
            </text>
          </view>
        </view>
        <view v-if="contact?.current_projects?.length" class="info-block">
          <text class="section-title">当前项目</text>
          <view class="list-items">
            <text v-for="(project, i) in contact.current_projects" :key="i" class="list-item">
              • {{ project }}
            </text>
          </view>
        </view>
        <view v-if="hasGoals" class="info-block">
          <text class="section-title">目标</text>
          <view class="goals-grid">
            <view v-if="contact?.short_term_goals?.length" class="goal-block">
              <text class="goal-label">短期目标</text>
              <view class="goal-list">
                <text v-for="(goal, i) in contact.short_term_goals" :key="i" class="goal-item">
                  🎯 {{ goal }}
                </text>
              </view>
            </view>
            <view v-if="contact?.long_term_goals?.length" class="goal-block">
              <text class="goal-label">长期目标</text>
              <view class="goal-list">
                <text v-for="(goal, i) in contact.long_term_goals" :key="i" class="goal-item">
                  🎯 {{ goal }}
                </text>
              </view>
            </view>
          </view>
        </view>
        <view v-if="hasResources" class="info-block">
          <text class="section-title">资源位</text>
          <view class="resources-grid">
            <view v-if="contact?.resource_needs?.length" class="resource-card needs">
              <text class="resource-title">需要资源</text>
              <view class="resource-list">
                <text v-for="(need, i) in contact.resource_needs" :key="i" class="resource-item">
                  • {{ need }}
                </text>
              </view>
            </view>
            <view v-if="contact?.resource_offers?.length" class="resource-card offers">
              <text class="resource-title">可提供资源</text>
              <view class="resource-list">
                <text v-for="(offer, i) in contact.resource_offers" :key="i" class="resource-item">
                  • {{ offer }}
                </text>
              </view>
            </view>
          </view>
        </view>
        <view v-if="hasEmotions" class="info-block">
          <text class="section-title">情绪状态</text>
          <EmotionSection v-if="contact?.excitement_points?.length" icon="🔥" label="兴奋点" :items="contact.excitement_points" color="orange" />
          <EmotionSection v-if="contact?.anxiety_points?.length" icon="😰" label="焦虑点" :items="contact.anxiety_points" color="gray" />
          <EmotionSection v-if="contact?.sensitive_points?.length" icon="⚠️" label="敏感点（避雷）" :items="contact.sensitive_points" color="red" />
        </view>
      </view>

      <!-- 互动历史 -->
      <view v-if="activeTab === 'timeline'" class="timeline-section">
        <view v-if="meetings.length === 0" class="empty-state">
          <text class="empty-icon">📅</text>
          <text class="empty-text">还没有会谈记录</text>
        </view>
        <view v-else class="timeline-list">
          <view v-for="meeting in meetings" :key="meeting.id" class="timeline-item">
            <view class="timeline-dot"></view>
            <view class="timeline-card">
              <view class="meeting-header">
                <text class="meeting-date">{{ formatDateTime(meeting.meeting_date) }}</text>
                <view class="meeting-tags">
                  <text v-if="meeting.scenario" class="scenario-tag">{{ meeting.scenario }}</text>
                  <text v-if="meeting.sentiment" class="sentiment-tag" :style="{ background: getSentimentColor(meeting.sentiment) + '20', color: getSentimentColor(meeting.sentiment) }">
                    {{ getSentimentLabel(meeting.sentiment) }}
                  </text>
                </view>
              </view>
              <view v-if="meeting.topics?.length" class="meeting-topics">
                <text v-for="(topic, i) in meeting.topics" :key="i" class="topic-chip">{{ topic }}</text>
              </view>
              <view v-if="meeting.key_facts?.length" class="meeting-section">
                <text class="section-label">关键事实</text>
                <view class="fact-list">
                  <text v-for="(fact, i) in meeting.key_facts" :key="i" class="fact-item">
                    • {{ typeof fact === 'string' ? fact : fact.fact }}
                  </text>
                </view>
              </view>
              <view v-if="meeting.my_commitments?.length || meeting.their_commitments?.length" class="commitments-row">
                <view v-if="meeting.my_commitments?.length" class="commitment-card my">
                  <text class="commitment-title">我的承诺</text>
                  <text v-for="(c, i) in meeting.my_commitments" :key="i" class="commitment-item">
                    • {{ typeof c === 'string' ? c : c.commitment }}
                  </text>
                </view>
                <view v-if="meeting.their_commitments?.length" class="commitment-card their">
                  <text class="commitment-title">对方承诺</text>
                  <text v-for="(c, i) in meeting.their_commitments" :key="i" class="commitment-item">
                    • {{ typeof c === 'string' ? c : c.commitment }}
                  </text>
                </view>
              </view>
              <view v-if="meeting.open_loops?.length || meeting.next_conversation_hooks?.length" class="hooks-card">
                <text class="hooks-title">续聊线索</text>
                <view class="hooks-list">
                  <text v-for="(loop, i) in (meeting.open_loops || [])" :key="'loop' + i" class="hook-item">
                    🔄 未完: {{ loop }}
                  </text>
                  <text v-for="(hook, i) in (meeting.next_conversation_hooks || [])" :key="'hook' + i" class="hook-item">
                    💬 下次可聊: {{ hook }}
                  </text>
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 行动建议 -->
      <view v-if="activeTab === 'playbook'" class="playbook-section">
        <view v-if="!playbook" class="empty-state">
          <text class="empty-icon">🎯</text>
          <text class="empty-text">暂无行动建议</text>
          <text class="empty-hint">记录更多对话后将自动生成</text>
        </view>
        <view v-else class="playbook-content">
          <PlaybookSection v-if="playbook.preferences?.length || playbook.taboos?.length" icon="❤️" title="送礼与关怀" color="pink">
            <view v-if="playbook.preferences?.length" class="playbook-block">
              <text class="playbook-label">偏好</text>
              <view class="playbook-tags">
                <text v-for="(pref, i) in playbook.preferences" :key="i" class="pref-tag">{{ pref }}</text>
              </view>
            </view>
            <view v-if="playbook.taboos?.length" class="playbook-block">
              <text class="playbook-label">禁忌</text>
              <view class="playbook-tags">
                <text v-for="(taboo, i) in playbook.taboos" :key="i" class="taboo-tag">{{ taboo }}</text>
              </view>
            </view>
            <view v-if="playbook.gift_recommendations" class="playbook-block">
              <text class="playbook-label">推荐礼物</text>
              <view class="gift-recommendations">
                <view v-for="(items, tier) in playbook.gift_recommendations" :key="tier" class="gift-tier">
                  <text class="tier-label">{{ tier === 'small' ? '小礼' : tier === 'medium' ? '中礼' : '正式' }}: </text>
                  <text class="tier-items">{{ Array.isArray(items) ? items.join(', ') : items }}</text>
                </view>
              </view>
            </view>
          </PlaybookSection>
          <PlaybookSection v-if="playbook.top_topics?.length || playbook.conversation_questions?.length" icon="💬" title="续聊钩子" color="blue">
            <view v-if="playbook.top_topics?.length" class="playbook-block">
              <text class="playbook-label">最投入话题</text>
              <view class="playbook-tags">
                <text v-for="(topic, i) in playbook.top_topics" :key="i" class="topic-tag-chip">{{ topic }}</text>
              </view>
            </view>
            <view v-if="playbook.conversation_questions?.length" class="playbook-block">
              <text class="playbook-label">下次可问</text>
              <view class="questions-list">
                <text v-for="(q, i) in playbook.conversation_questions" :key="i" class="question-item">• {{ q }}</text>
              </view>
            </view>
          </PlaybookSection>
          <PlaybookSection v-if="playbook.how_i_can_help_them?.length || playbook.how_they_can_help_me?.length" icon="🤝" title="合作地图" color="green">
            <view class="collab-grid">
              <view v-if="playbook.how_i_can_help_them?.length" class="collab-block">
                <text class="collab-label">我如何帮他</text>
                <view class="collab-list">
                  <text v-for="(item, i) in playbook.how_i_can_help_them" :key="i" class="collab-item">• {{ item }}</text>
                </view>
              </view>
              <view v-if="playbook.how_they_can_help_me?.length" class="collab-block">
                <text class="collab-label">他如何帮我</text>
                <view class="collab-list">
                  <text v-for="(item, i) in playbook.how_they_can_help_me" :key="i" class="collab-item">• {{ item }}</text>
                </view>
              </view>
            </view>
          </PlaybookSection>
          <PlaybookSection icon="🔥" title="关系健康" color="purple">
            <view class="health-info">
              <view v-if="playbook.relationship_stage" class="health-item">
                <text class="health-label">阶段</text>
                <text class="health-value">{{ getRelationshipLabel(playbook.relationship_stage) }}</text>
              </view>
              <view v-if="playbook.temperature_score !== null" class="health-item">
                <text class="health-label">温度分</text>
                <text class="health-value">{{ playbook.temperature_score }}/100</text>
              </view>
            </view>
            <view v-if="playbook.next_action" class="next-action-card">
              <text class="next-action-label">建议下一步</text>
              <text class="next-action-text">{{ typeof playbook.next_action === 'string' ? playbook.next_action : playbook.next_action.action }}</text>
            </view>
          </PlaybookSection>
        </view>
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view class="footer-bar">
      <button class="footer-btn" @click="handleExport">
        <text class="footer-btn-icon">📥</text>
        <text>导出Markdown</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onLoad } from '@dcloudio/uni-app';
import { useContactStore } from '@/store/contact';
import {
  formatDate,
  formatDateTime,
  getInitials,
  getRelationshipLabel,
  getRelationshipColor,
  getTemperatureColor,
  getSentimentLabel,
  getSentimentColor
} from '@/utils';
import type { Contact, Meeting, ActionPlaybook } from '@/types';

const contactStore = useContactStore();

const contact = ref<Contact | null>(null);
const meetings = ref<Meeting[]>([]);
const playbook = ref<ActionPlaybook | null>(null);
const activeTab = ref<'identity' | 'status' | 'timeline' | 'playbook'>('identity');
const contactId = ref<number>(0);

const tabs = computed(() => [
  { key: 'identity' as const, label: '身份信息' },
  { key: 'status' as const, label: '当前状态' },
  { key: 'timeline' as const, label: '互动历史', count: meetings.value.length },
  { key: 'playbook' as const, label: '行动建议' },
]);

// 计算属性
const hasContactMethods = computed(() =>
  contact.value?.phone || contact.value?.email || contact.value?.wechat
);

const hasEducation = computed(() =>
  contact.value?.education_school || contact.value?.education_major || contact.value?.education_degree
);

const hasCommunication = computed(() =>
  contact.value?.preferred_contact_method || contact.value?.preferred_contact_time || contact.value?.communication_style
);

const hasWork = computed(() =>
  contact.value?.current_company || contact.value?.current_position || contact.value?.current_industry
);

const hasGoals = computed(() =>
  contact.value?.short_term_goals?.length || contact.value?.long_term_goals?.length
);

const hasResources = computed(() =>
  contact.value?.resource_needs?.length || contact.value?.resource_offers?.length
);

const hasEmotions = computed(() =>
  contact.value?.excitement_points?.length || contact.value?.anxiety_points?.length || contact.value?.sensitive_points?.length
);

const identityFields = computed(() => [
  { label: '昵称', value: contact.value?.nickname },
  { label: '性别', value: contact.value?.gender },
  { label: '年龄段', value: contact.value?.age_group },
  { label: '家乡', value: contact.value?.hometown },
  { label: '常驻城市', value: contact.value?.city },
  { label: 'LinkedIn', value: contact.value?.linkedin },
]);

const educationFields = computed(() => [
  { label: '学校', value: contact.value?.education_school },
  { label: '专业', value: contact.value?.education_major },
  { label: '学位', value: contact.value?.education_degree },
]);

const communicationFields = computed(() => [
  { label: '偏好方式', value: contact.value?.preferred_contact_method },
  { label: '偏好时间', value: contact.value?.preferred_contact_time },
  { label: '沟通风格', value: contact.value?.communication_style },
]);

const workFields = computed(() => [
  { label: '公司', value: contact.value?.current_company },
  { label: '职位', value: contact.value?.current_position },
  { label: '行业', value: contact.value?.current_industry },
]);

async function loadData() {
  const data = await contactStore.loadContactDetail(contactId.value);
  contact.value = data.contact;
  meetings.value = data.meetings;
  playbook.value = data.action_playbook;
}

function handleExport() {
  contactStore.exportContact(contactId.value, contact.value?.name || 'contact');
}

onLoad((options: any) => {
  if (options.id) {
    contactId.value = parseInt(options.id);
    loadData();
  }
});
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F5;
  padding-bottom: 120rpx;
}

.header-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40rpx 30rpx;
  color: #FFFFFF;
}

.avatar-section {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
}

.avatar-text {
  font-size: 44rpx;
  font-weight: bold;
  color: #FFFFFF;
}

.header-info {
  flex: 1;
}

.contact-name {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  margin-bottom: 8rpx;
}

.contact-work {
  display: block;
  font-size: 28rpx;
  opacity: 0.9;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.stage-tag {
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  font-weight: 500;
}

.temp-score {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.temp-label {
  font-size: 24rpx;
  opacity: 0.8;
}

.temp-value {
  font-size: 36rpx;
  font-weight: bold;
}

.contact-methods {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  padding: 24rpx 30rpx;
}

.method-item {
  display: flex;
  align-items: center;
  gap: 10rpx;
  font-size: 26rpx;
  color: #666666;
}

.method-icon {
  font-size: 32rpx;
}

.card {
  background: #FFFFFF;
  margin: 20rpx 30rpx;
  border-radius: 20rpx;
  padding: 30rpx;
}

.tabs {
  display: flex;
  background: #FFFFFF;
  margin: 20rpx 30rpx 0;
  border-radius: 20rpx 20rpx 0 0;
  overflow: hidden;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 28rpx 0;
  font-size: 28rpx;
  color: #666666;
  border-bottom: 4rpx solid transparent;

  &.active {
    color: #007AFF;
    border-bottom-color: #007AFF;
    font-weight: 500;
  }
}

.tab-count {
  font-size: 24rpx;
  margin-left: 4rpx;
}

.tab-content {
  background: #FFFFFF;
  margin: 0 30rpx;
  border-radius: 0 0 20rpx 20rpx;
  padding: 30rpx;
  min-height: 400rpx;
}

/* 信息区块 */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 40rpx;
}

.info-block {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.section-title {
  font-size: 26rpx;
  color: #999999;
  font-weight: 500;
}

.section-text {
  font-size: 28rpx;
  color: #333333;
  line-height: 1.6;
}

.info-row {
  display: flex;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #F0F0F0;

  &:last-child {
    border-bottom: none;
  }
}

.info-label {
  width: 200rpx;
  font-size: 26rpx;
  color: #999999;
}

.info-value {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
}

/* 标签 */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.topic-tag {
  padding: 10rpx 20rpx;
  background: #E3F2FD;
  color: #007AFF;
  border-radius: 20rpx;
  font-size: 24rpx;
}

/* 列表项 */
.list-items {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.list-item {
  font-size: 28rpx;
  color: #333333;
}

/* 目标 */
.goals-grid {
  display: flex;
  gap: 30rpx;
}

.goal-block {
  flex: 1;
}

.goal-label {
  display: block;
  font-size: 26rpx;
  color: #666666;
  margin-bottom: 12rpx;
}

.goal-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.goal-item {
  font-size: 26rpx;
  color: #333333;
}

/* 资源 */
.resources-grid {
  display: flex;
  gap: 20rpx;
}

.resource-card {
  flex: 1;
  padding: 24rpx;
  border-radius: 16rpx;

  &.needs {
    background: #FFF3E0;
  }

  &.offers {
    background: #E8F5E9;
  }
}

.resource-title {
  display: block;
  font-size: 26rpx;
  font-weight: 500;
  margin-bottom: 12rpx;

  .needs & {
    color: #E65100;
  }

  .offers & {
    color: #1B5E20;
  }
}

.resource-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.resource-item {
  font-size: 26rpx;

  .needs & {
    color: #E65100;
  }

  .offers & {
    color: #1B5E20;
  }
}

/* 情绪 */
.emotion-block {
  padding: 20rpx;
  background: #F5F5F5;
  border-radius: 12rpx;
  margin-bottom: 16rpx;
}

.emotion-label {
  font-size: 26rpx;
  color: #666666;
  margin-bottom: 10rpx;
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

  &.orange {
    background: #FFE0B2;
    color: #E65100;
  }

  &.gray {
    background: #E0E0E0;
    color: #424242;
  }

  &.red {
    background: #FFCDD2;
    color: #C62828;
  }
}

/* 时间线 */
.timeline-list {
  display: flex;
  flex-direction: column;
  gap: 40rpx;
}

.timeline-item {
  display: flex;
  position: relative;
}

.timeline-dot {
  width: 24rpx;
  height: 24rpx;
  background: #667eea;
  border-radius: 50%;
  margin-top: 10rpx;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.timeline-card {
  flex: 1;
  background: #F8F8F8;
  border-radius: 16rpx;
  padding: 24rpx;
}

.meeting-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.meeting-date {
  font-size: 26rpx;
  color: #007AFF;
  font-weight: 500;
}

.meeting-tags {
  display: flex;
  gap: 12rpx;
}

.scenario-tag, .sentiment-tag {
  padding: 6rpx 16rpx;
  border-radius: 12rpx;
  font-size: 22rpx;
}

.scenario-tag {
  background: #E0E0E0;
  color: #424242;
}

.meeting-topics {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-bottom: 16rpx;
}

.topic-chip {
  padding: 8rpx 16rpx;
  background: #E3F2FD;
  color: #007AFF;
  border-radius: 16rpx;
  font-size: 24rpx;
}

.meeting-section, .commitments-row, .hooks-card {
  background: #FFFFFF;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 12rpx;
}

.section-label {
  display: block;
  font-size: 24rpx;
  color: #999999;
  margin-bottom: 10rpx;
}

.fact-list, .commitment-list, .hooks-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.fact-item, .commitment-item, .hook-item {
  font-size: 26rpx;
  color: #666666;
}

.commitments-row {
  display: flex;
  gap: 20rpx;
}

.commitment-card {
  flex: 1;
  padding: 16rpx;
  border-radius: 12rpx;

  &.my {
    background: #E3F2FD;
  }

  &.their {
    background: #E8F5E9;
  }
}

.commitment-title {
  display: block;
  font-size: 22rpx;
  font-weight: 500;
  margin-bottom: 8rpx;

  .my & {
    color: #007AFF;
  }

  .their & {
    color: #2E7D32;
  }
}

.commitment-item {
  display: block;
  font-size: 24rpx;

  .my & {
    color: #007AFF;
  }

  .their & {
    color: #2E7D32;
  }
}

.hooks-title {
  display: block;
  font-size: 24rpx;
  color: #F57C00;
  margin-bottom: 10rpx;
}

.hook-item {
  display: block;
  font-size: 24rpx;
  color: #666666;
}

/* 行动建议 */
.playbook-content {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.playbook-block {
  margin-bottom: 20rpx;
}

.playbook-label {
  display: block;
  font-size: 26rpx;
  color: #666666;
  margin-bottom: 12rpx;
}

.playbook-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
}

.pref-tag {
  padding: 10rpx 20rpx;
  background: #FCE4EC;
  color: #C2185B;
  border-radius: 16rpx;
  font-size: 24rpx;
}

.taboo-tag {
  padding: 10rpx 20rpx;
  background: #FFCDD2;
  color: #C62828;
  border-radius: 16rpx;
  font-size: 24rpx;
}

.topic-tag-chip {
  padding: 10rpx 20rpx;
  background: #E3F2FD;
  color: #007AFF;
  border-radius: 16rpx;
  font-size: 24rpx;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.question-item {
  font-size: 26rpx;
  color: #007AFF;
}

.gift-recommendations {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.gift-tier {
  font-size: 26rpx;
  color: #C2185B;
}

.tier-label {
  font-weight: 500;
}

.collab-grid {
  display: flex;
  gap: 20rpx;
}

.collab-block {
  flex: 1;
}

.collab-label {
  display: block;
  font-size: 26rpx;
  color: #1B5E20;
  margin-bottom: 12rpx;
}

.collab-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.collab-item {
  font-size: 26rpx;
  color: #1B5E20;
}

.health-info {
  display: flex;
  gap: 40rpx;
}

.health-item {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.health-label {
  font-size: 24rpx;
  color: #7B1FA2;
}

.health-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #7B1FA2;
}

.next-action-card {
  background: #F3E5F5;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-top: 16rpx;
}

.next-action-label {
  display: block;
  font-size: 24rpx;
  color: #7B1FA2;
  margin-bottom: 8rpx;
}

.next-action-text {
  font-size: 28rpx;
  color: #7B1FA2;
  line-height: 1.5;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80rpx 0;
}

.empty-icon {
  display: block;
  font-size: 120rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  display: block;
  font-size: 28rpx;
  color: #999999;
}

.empty-hint {
  display: block;
  font-size: 24rpx;
  color: #CCCCCC;
  margin-top: 10rpx;
}

/* 底部栏 */
.footer-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #FFFFFF;
  padding: 20rpx 30rpx;
  border-top: 1rpx solid #EEEEEE;
  display: flex;
  gap: 20rpx;
}

.footer-btn {
  flex: 1;
  height: 80rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  font-size: 28rpx;
  color: #FFFFFF;
  border: none;
}

.footer-btn-icon {
  font-size: 32rpx;
}
</style>
