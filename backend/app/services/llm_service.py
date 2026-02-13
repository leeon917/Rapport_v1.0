"""
LLM service for extracting structured contact information from conversation text.
"""
import json
from typing import Optional, Dict, Any
from openai import OpenAI
from app.core.config import settings


class LLMService:
    """Service for LLM-based text extraction and structuring."""

    def __init__(self):
        """Initialize the LLM service with OpenAI-compatible client."""
        self.client = OpenAI(
            api_key=settings.llm_api_key or "dummy-key",
            base_url=settings.llm_base_url
        )
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens
        self.max_retries = settings.llm_max_retries

    def _create_system_prompt(self) -> str:
        """Create the system prompt for contact extraction."""
        return """你是一个专业的联系人信息提取专家。你的任务是从对话文本中提取结构化的联系人信息。

请严格按照以下JSON Schema返回结果，不要添加任何额外的文字说明。

返回的JSON结构：
{
  "contact": {
    "name": "姓名（从对话中推断）",
    "nickname": "昵称",
    "gender": "性别",
    "age_group": "年龄段（如：20-30, 30-40等）",
    "city": "常驻城市",
    "phone": "电话",
    "email": "邮箱",
    "wechat": "微信号",
    "linkedin": "LinkedIn链接",
    "education_school": "毕业学校",
    "education_major": "专业",
    "education_degree": "学位",
    "career_summary": "职业概述（1-3句话）",
    "preferred_contact_method": "偏好联系方式（微信/电话/邮件）",
    "preferred_contact_time": "偏好联系时间",
    "communication_style": "沟通风格（直接/委婉等）",
    "current_company": "当前公司",
    "current_position": "当前职位",
    "current_industry": "所在行业",
    "current_location": "当前工作地点",
    "startup_status": "创业状态",
    "focus_topics": ["关注话题列表"],
    "current_projects": ["当前项目列表"],
    "short_term_goals": ["短期目标列表"],
    "long_term_goals": ["长期目标列表"],
    "resource_needs": ["需要资源列表"],
    "resource_offers": ["可提供资源列表"],
    "excitement_points": ["近期兴奋点"],
    "anxiety_points": ["近期焦虑点"],
    "sensitive_points": ["敏感话题"]
  },
  "meeting": {
    "meeting_date": "会议日期（推断或使用当前日期）",
    "location": "会议地点",
    "scenario": "会议场景（如：商务午餐、行业峰会、咖啡见面等）",
    "topics": ["讨论的主题列表"],
    "key_facts": [
      {"fact": "事实描述", "category": "分类"}
    ],
    "sentiment": "对话情绪（positive/neutral/negative）",
    "my_commitments": [
      {"commitment": "承诺内容", "deadline": "截止日期（如有）"}
    ],
    "their_commitments": [
      {"commitment": "对方承诺", "deadline": "截止日期（如有）"}
    ],
    "open_loops": ["未完成的话题列表"],
    "next_conversation_hooks": ["下次可以聊的话题/问题列表"]
  },
  "action_playbook": {
    "gift_care": {
      "preferences": ["喜好清单"],
      "taboos": ["禁忌/雷点"],
      "gift_occasions": ["送礼时机"],
      "gift_recommendations": {
        "small": ["小礼物推荐"],
        "medium": ["中等礼物推荐"],
        "formal": ["正式礼物推荐"]
      }
    },
    "conversation_hooks": {
      "top_topics": ["最投入的Top3话题"],
      "open_loops": ["未完结线索"],
      "conversation_questions": ["下次可问的问题5-10个"],
      "conversation_avoid": ["避免的话术/敏感点"]
    },
    "collaboration_map": {
      "how_i_can_help_them": ["我可以帮到他的方式"],
      "how_they_can_help_me": ["他可以帮到我的方式"],
      "exchange_boundaries": ["交换原则/边界"],
      "contact_rhythm": {
        "frequency": "建议联系频率",
        "style": "沟通风格建议"
      }
    },
    "relationship_health": {
      "relationship_stage": "关系阶段（new/acquaintance/friend/ally/key_partner）",
      "temperature_score": 75,
      "recent_risks": ["近期风险"],
      "next_action": {
        "action": "建议下一步动作",
        "timing": "建议时间",
        "reason": "原因"
      }
    }
  }
}

注意：
1. 如果某个字段无法从对话中推断，请使用null或空数组
2. 所有字符串值使用简体中文
3. 日期格式使用ISO 8601（YYYY-MM-DD）
4. 尽量提取准确信息，不要编造
5. key_facts应该是对方明确表达的事实、决策或偏好
6. action_playbook应该是从对话内容中提炼的可执行建议"""

    def extract_contact_info(
        self,
        conversation_text: str,
        known_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured contact information from conversation text.

        Args:
            conversation_text: The raw conversation text
            known_name: Optional known name of the contact

        Returns:
            Dictionary with extracted contact, meeting, and action_playbook data
        """
        user_prompt = f"请从以下对话文本中提取联系人信息：\n\n{conversation_text}"
        if known_name:
            user_prompt += f"\n\n（对方姓名：{known_name}）"

        system_prompt = self._create_system_prompt()

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    response_format={"type": "json_object"}
                )

                result = response.choices[0].message.content
                parsed_result = json.loads(result)

                # Validate structure
                if "contact" not in parsed_result:
                    parsed_result["contact"] = {}
                if "meeting" not in parsed_result:
                    parsed_result["meeting"] = {}
                if "action_playbook" not in parsed_result:
                    parsed_result["action_playbook"] = {}

                return parsed_result

            except json.JSONDecodeError as e:
                if attempt < self.max_retries:
                    continue
                raise ValueError(f"Failed to parse LLM response as JSON after {self.max_retries} retries: {e}")

            except Exception as e:
                if attempt < self.max_retries:
                    continue
                raise ValueError(f"LLM extraction failed after {self.max_retries} retries: {e}")

        # Should not reach here
        raise RuntimeError("Unexpected error in LLM extraction")

    def update_action_playbook(
        self,
        existing_playbook: Dict[str, Any],
        new_meeting_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update action playbook with new meeting information.

        Args:
            existing_playbook: Current action playbook
            new_meeting_data: New meeting data to incorporate

        Returns:
            Updated action playbook
        """
        prompt = f"""请根据以下新的会谈信息，更新联系人的行动剧本（Action Playbook）。

现有行动剧本：
{json.dumps(existing_playbook, ensure_ascii=False, indent=2)}

新的会谈信息：
{json.dumps(new_meeting_data, ensure_ascii=False, indent=2)}

请返回更新后的完整行动剧本，保持相同的JSON结构。注意：
1. 合并新旧信息，不要丢失重要的历史数据
2. 如果新旧信息冲突，以最新的为准
3. 增强推荐的可执行性
4. 保持JSON格式正确"""

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是联系人关系管理专家，负责维护和更新行动剧本。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    response_format={"type": "json_object"}
                )

                result = response.choices[0].message.content
                return json.loads(result)

            except json.JSONDecodeError:
                if attempt < self.max_retries:
                    continue
                # Fallback: return existing playbook
                return existing_playbook

            except Exception:
                if attempt < self.max_retries:
                    continue
                return existing_playbook


# Global instance
llm_service = LLMService()
