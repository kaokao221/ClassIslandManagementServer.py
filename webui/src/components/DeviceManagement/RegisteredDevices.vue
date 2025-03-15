<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            已注册设备管理
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="搜索客户端 (UID)"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="filteredClients"
              :search="search"
              class="elevation-1"
              :loading="loading"
              loading-text="加载客户端数据..."
              no-data-text="没有已注册的客户端"
              show-select
              v-model="selectedClients"
            >
              <template v-slot:item.status="{ item }">
                <v-chip :color="item.status === 'online' ? 'success' : 'error'" dark>
                  {{ item.status }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn icon @click="restartClient(item.uid)">
                  <v-icon>mdi-restart</v-icon>
                </v-btn>
                <v-btn icon @click="sendNotificationDialog(item.uid)">
                  <v-icon>mdi-bell-ring</v-icon>
                </v-btn>
                <!-- 可以添加更多操作按钮 -->
              </template>
            </v-data-table>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <DeviceBulkActions
              :selected-clients="selectedClients"
              @clients-restarted="refreshClients"
              @notifications-sent="refreshClients"  
            />
            <!-- 假设刷新列表后更新状态 -->
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- 发送通知对话框 -->
    <v-dialog v-model="notificationDialog" max-width="500px">
      <v-card>
        <v-card-title class="headline">发送通知给客户端 {{ notificationClientUid }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="messageMask" label="消息掩码" required></v-text-field>
          <v-textarea v-model="messageContent" label="消息内容" required></v-textarea>
          <!-- 可以添加更多通知选项，例如图标、语音、特效等 -->
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="notificationDialog = false">取消</v-btn>
          <v-btn color="primary" text @click="sendNotification">发送</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import api from '@/services/api';
import DeviceBulkActions from './DeviceBulkActions.vue';

export default {
  name: 'RegisteredDevices',
  components: {
    DeviceBulkActions,
  },
  data() {
    return {
      loading: false,
      search: '',
      headers: [
        { text: 'UID', value: 'uid' },
        { text: '状态', value: 'status' },
        { text: '操作', value: 'actions', sortable: false },
      ],
      clients: [],
      selectedClients: [],
      notificationDialog: false,
      notificationClientUid: null,
      messageMask: '',
      messageContent: '',
    };
  },
  computed: {
    filteredClients() {
      return this.clients; //  搜索功能已由 v-data-table 的 :search 属性实现，如果需要更复杂的搜索/筛选，可以在这里实现
    },
  },
  mounted() {
    this.fetchClients();
  },
  methods: {
    async fetchClients() {
      this.loading = true;
      try {
        const clientsList = await api.listClients();
        const clientStatuses = await api.getClientStatuses();

        // 合并客户端列表和状态信息
        this.clients = clientsList.data.map(uid => {
          const statusInfo = clientStatuses.data.find(s => s.uid === uid);
          return { uid: uid, status: statusInfo ? statusInfo.status : 'unknown' };
        });

      } catch (error) {
        console.error('Failed to fetch clients:', error);
        // TODO: 显示错误提示
      } finally {
        this.loading = false;
      }
    },
    refreshClients() {
      this.fetchClients(); // 重新加载客户端列表
      this.selectedClients = []; // 清空已选
    },
    async restartClient(clientUid) {
      try {
        await api.restartClient(clientUid);
        this.$vToastify.success(`客户端 ${clientUid} 重启指令已发送!`);
        // 可以考虑在重启后更新客户端状态，或者刷新列表
      } catch (error) {
        console.error('Failed to restart client:', error);
        this.$vToastify.error(`重启客户端 ${clientUid} 失败!`);
      }
    },
    sendNotificationDialog(clientUid) {
      this.notificationClientUid = clientUid;
      this.notificationDialog = true;
      this.messageMask = '';
      this.messageContent = '';
    },
    async sendNotification() {
      try {
        await api.sendClientNotification(this.notificationClientUid, this.messageMask, this.messageContent);
        this.$vToastify.success(`通知已发送给客户端 ${this.notificationClientUid}!`);
        this.notificationDialog = false;
      } catch (error) {
        console.error('Failed to send notification:', error);
        this.$vToastify.error(`发送通知给客户端 ${this.notificationClientUid} 失败!`);
      }
    },
  },
};
</script>