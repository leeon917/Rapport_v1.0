import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { ContactListItem, Contact, ContactWithTimeline } from '@/types';
import { contactsApi } from '@/api';

export const useContactStore = defineStore('contact', () => {
  const contacts = ref<ContactListItem[]>([]);
  const currentContact = ref<ContactWithTimeline | null>(null);
  const loading = ref(false);
  const searchKeyword = ref('');

  // 加载联系人列表
  async function loadContacts(search?: string) {
    loading.value = true;
    try {
      if (search !== undefined) {
        searchKeyword.value = search;
      }
      contacts.value = await contactsApi.list(search || searchKeyword.value);
    } catch (error) {
      uni.showToast({
        title: '加载失败',
        icon: 'none'
      });
      throw error;
    } finally {
      loading.value = false;
    }
  }

  // 加载联系人详情
  async function loadContactDetail(id: number) {
    loading.value = true;
    try {
      currentContact.value = await contactsApi.getTimeline(id);
    } catch (error) {
      uni.showToast({
        title: '加载失败',
        icon: 'none'
      });
      throw error;
    } finally {
      loading.value = false;
    }
  }

  // 创建联系人
  async function createContact(data: { name?: string }) {
    loading.value = true;
    try {
      await contactsApi.create(data);
      await loadContacts();
      uni.showToast({
        title: '创建成功',
        icon: 'success'
      });
    } catch (error) {
      uni.showToast({
        title: '创建失败',
        icon: 'none'
      });
      throw error;
    } finally {
      loading.value = false;
    }
  }

  // 创建会面记录
  async function createMeeting(data: {
    contact_name?: string;
    raw_text: string;
    location?: string;
    scenario?: string;
  }) {
    loading.value = true;
    try {
      await contactsApi.create(data);
      await loadContacts();
      uni.showToast({
        title: '记录已添加',
        icon: 'success'
      });
    } catch (error) {
      uni.showToast({
        title: '添加失败',
        icon: 'none'
      });
      throw error;
    } finally {
      loading.value = false;
    }
  }

  // 导出联系人
  async function exportContact(id: number, name: string) {
    try {
      const markdown = await contactsApi.exportMarkdown(id);
      const fileName = `${name || 'contact'}_${id}.md`;

      // H5环境下载
      // #ifdef H5
      const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      // #endif

      // 小程序环境复制到剪贴板
      // #ifdef MP-WEIXIN
      uni.setClipboardData({
        data: markdown,
        success: () => {
          uni.showModal({
            title: '导出成功',
            content: '内容已复制到剪贴板，请保存到笔记应用'
          });
        }
      });
      // #endif

      uni.showToast({
        title: '导出成功',
        icon: 'success'
      });
    } catch (error) {
      uni.showToast({
        title: '导出失败',
        icon: 'none'
      });
    }
  }

  // 清空当前联系人
  function clearCurrentContact() {
    currentContact.value = null;
  }

  return {
    contacts,
    currentContact,
    loading,
    searchKeyword,
    loadContacts,
    loadContactDetail,
    createContact,
    createMeeting,
    exportContact,
    clearCurrentContact
  };
});
