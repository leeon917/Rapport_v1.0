import request from './request';
import type {
  User,
  Contact,
  ContactListItem,
  ContactWithTimeline,
  Meeting,
  ActionPlaybook,
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  CreateMeetingRequest,
  CreateContactRequest
} from '@/types';

// ==================== 认证 API ====================
export const authApi = {
  // 注册
  register: (data: RegisterRequest): Promise<User> => {
    return request.post('/auth/register', data);
  },

  // 登录
  login: (data: LoginRequest): Promise<TokenResponse> => {
    return request.post('/auth/login', data);
  }
};

// ==================== 联系人 API ====================
export const contactsApi = {
  // 获取联系人列表
  list: (search?: string): Promise<ContactListItem[]> => {
    return request.get('/contacts', search ? { search } : undefined);
  },

  // 获取联系人详情
  get: (id: number): Promise<Contact> => {
    return request.get(`/contacts/${id}`);
  },

  // 创建联系人
  create: (data: CreateContactRequest): Promise<Contact> => {
    return request.post('/contacts', data);
  },

  // 更新联系人
  update: (id: number, data: Partial<Contact>): Promise<Contact> => {
    return request.put(`/contacts/${id}`, data);
  },

  // 删除联系人
  delete: (id: number): Promise<void> => {
    return request.delete(`/contacts/${id}`);
  },

  // 获取联系人详情（含时间线）
  getTimeline: (id: number): Promise<ContactWithTimeline> => {
    return request.get(`/contacts/${id}/timeline`);
  },

  // 导出Markdown
  exportMarkdown: (id: number): Promise<string> => {
    return request.getText(`/contacts/${id}/export`);
  },

  // 添加会面记录
  addMeeting: (contactId: number, data: CreateMeetingRequest): Promise<Meeting> => {
    return request.post(`/contacts/${contactId}/meetings`, data);
  },

  // 获取会面记录列表
  getMeetings: (contactId: number): Promise<Meeting[]> => {
    return request.get(`/contacts/${contactId}/meetings`);
  }
};

// ==================== 会面 API ====================
export const meetingsApi = {
  // 创建会面记录
  create: (data: CreateMeetingRequest): Promise<Meeting> => {
    return request.post('/meetings', data);
  },

  // 获取会面记录列表
  list: (contactId?: number): Promise<Meeting[]> => {
    return request.get('/meetings', contactId ? { contact_id: contactId } : undefined);
  },

  // 获取会面详情
  get: (id: number): Promise<Meeting> => {
    return request.get(`/meetings/${id}`);
  }
};

export default { authApi, contactsApi, meetingsApi };
