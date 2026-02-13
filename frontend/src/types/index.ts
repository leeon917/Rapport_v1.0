// 联系人类型
export interface Contact {
  id: number;
  name: string | null;
  nickname: string | null;
  gender: string | null;
  age_group: string | null;
  hometown: string | null;
  city: string | null;
  phone: string | null;
  email: string | null;
  wechat: string | null;
  linkedin: string | null;
  education_school: string | null;
  education_major: string | null;
  education_degree: string | null;
  career_summary: string | null;
  preferred_contact_method: string | null;
  preferred_contact_time: string | null;
  communication_style: string | null;
  current_company: string | null;
  current_position: string | null;
  current_industry: string | null;
  current_location: string | null;
  startup_status: string | null;
  focus_topics: string[] | null;
  current_projects: string[] | null;
  short_term_goals: string[] | null;
  long_term_goals: string[] | null;
  resource_needs: string[] | null;
  resource_offers: string[] | null;
  excitement_points: string[] | null;
  anxiety_points: string[] | null;
  sensitive_points: string[] | null;
  last_meeting_date: string | null;
  last_verified_at: string | null;
  relationship_stage: string | null;
  temperature_score: number | null;
  created_at: string;
  updated_at: string | null;
}

// 联系人列表项
export interface ContactListItem {
  id: number;
  name: string | null;
  current_company: string | null;
  current_position: string | null;
  last_meeting_date: string | null;
  relationship_stage: string | null;
  temperature_score: number | null;
}

// 会面/会议记录
export interface Meeting {
  id: number;
  contact_id: number;
  meeting_date: string;
  location: string | null;
  scenario: string | null;
  raw_text: string;
  topics: string[] | null;
  key_facts: Array<{ fact: string; category?: string }> | null;
  sentiment: string | null;
  my_commitments: Array<{ commitment: string; deadline?: string }> | null;
  their_commitments: Array<{ commitment: string; deadline?: string }> | null;
  open_loops: string[] | null;
  next_conversation_hooks: string[] | null;
  status: 'processing' | 'completed' | 'failed';
  error_message: string | null;
  created_at: string;
}

// 行动剧本
export interface ActionPlaybook {
  id: number;
  contact_id: number;
  preferences: string[] | null;
  taboos: string[] | null;
  gift_occasions: string[] | null;
  gift_recommendations: Record<string, string[]> | null;
  top_topics: string[] | null;
  open_loops: string[] | null;
  conversation_questions: string[] | null;
  conversation_avoid: string[] | null;
  how_i_can_help_them: string[] | null;
  how_they_can_help_me: string[] | null;
  exchange_boundaries: string[] | null;
  contact_rhythm: Record<string, any> | null;
  relationship_stage: string | null;
  temperature_score: number | null;
  recent_risks: string[] | null;
  next_action: Record<string, any> | null;
  evidence_refs: Record<string, any> | null;
  last_updated_at: string | null;
  created_at: string;
}

// 联系人详情（含时间线和行动剧本）
export interface ContactWithTimeline {
  contact: Contact;
  meetings: Meeting[];
  action_playbook: ActionPlaybook | null;
}

// 登录请求
export interface LoginRequest {
  email: string;
  password: string;
}

// 注册请求
export interface RegisterRequest {
  email: string;
  password: string;
}

// Token响应
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// 创建会面请求
export interface CreateMeetingRequest {
  contact_name?: string;
  raw_text: string;
  meeting_date?: string;
  location?: string;
  scenario?: string;
}

// 创建联系人请求
export interface CreateContactRequest {
  name?: string;
  nickname?: string;
  phone?: string;
  email?: string;
  wechat?: string;
  current_company?: string;
  current_position?: string;
}

// API响应包装
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}
