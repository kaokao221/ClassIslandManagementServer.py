/* eslint-disable no-unused-vars */
import axios from 'axios';

const API_BASE = process.env.VUE_APP_CIMS_API_BASE + '/api/v1';
const CMD_BASE = process.env.VUE_APP_CIMS_CMD_BASE + '/command';

const api = axios.create(); // 可以配置 axios 实例的默认行为，例如超时时间、拦截器等
const cmdApi = axios.create();

// 请求拦截器 (可选，例如统一处理 token)
// api.interceptors.request.use(...)
// cmdApi.interceptors.request.use(...)

// 响应拦截器 (统一处理错误)
const handleResponseError = (error) => {
  console.error('API Error:', error);
  // TODO: 可以根据错误状态码进行统一处理，例如显示全局错误提示
  return Promise.reject(error);
};

api.interceptors.response.use(response => response, handleResponseError);
cmdApi.interceptors.response.use(response => response, handleResponseError);


export default {
  // 客户端 API
  getClientManifest(clientUid, version) {
    return api.get(`/client/${clientUid}/manifest`, { params: { version } });
  },
  getClientResource(resourceType, name) {
    return api.get(`/client/${resourceType}`, { params: { name } });
  },

  // 服务器指令 API - 配置文件处理
  createConfigFile(resourceType, name) {
    return cmdApi.get(`/datas/${resourceType}/create`, { params: { name } }); //  文档写的是 GET，但创建操作用 POST/PUT 更语义化，需要确认
  },
  deleteConfigFile(resourceType, name) {
    return cmdApi.delete(`/datas/${resourceType}/delete`, { params: { name } });
  },
  listConfigFiles(resourceType) {
    return cmdApi.get(`/datas/${resourceType}/list`);
  },
  renameConfigFile(resourceType, name, target) {
    return cmdApi.get(`/datas/${resourceType}/rename`, { params: { name, target } });
  },
  writeFileConfig(resourceType, name, request) {
    return cmdApi.post(`/datas/${resourceType}/write`, { name, request }); // 文档写的是 GET/POST/PUT,  POST/PUT 更语义化
  },

  // 服务器指令 API - 服务器配置处理
  getServerSettings() {
    return cmdApi.get('/server/settings');
  },
  updateServerSettings(request) {
    return cmdApi.post('/server/settings', request); // 文档写的是 POST/PUT, POST/PUT 更语义化
  },

  // 服务器指令 API - 客户端信息处理
  listClients() {
    return cmdApi.get('/clients/list');
  },
  getClientStatuses() {
    return cmdApi.get('/clients/status');
  },
  preRegisterClient(request) {
    return cmdApi.post('/clients/pre_register', request); // 文档写的是 GET/POST, POST 更语义化
  },

  // 服务器指令 API - 指令
  restartClient(clientUid) {
    return cmdApi.get(`/client/${clientUid}/restart`);
  },
  sendClientNotification(clientUid, messageMask, messageContent, options) {
    return cmdApi.get(`/client/${clientUid}/send_notification`, {
      params: {
        message_mask: messageMask,
        message_content: messageContent,
        ...options // overlay_icon_left, overlay_icon_right, is_emergency, etc.
      }
    });
  },
};