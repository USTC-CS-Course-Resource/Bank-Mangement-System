import Notifications from "./Notifications.vue";

const NotificationStore = {
  state: [], // here the notifications will be added
  settings: {
    overlap: false,
    verticalAlign: "top",
    horizontalAlign: "right",
    type: "info",
    timeout: 1,
    closeOnClick: true,
    showClose: true
  },
  setOptions(options) {
    this.settings = Object.assign(this.settings, options);
  },
  removeNotification(timestamp) {
    const indexToDelete = this.state.findIndex(n => n.timestamp === timestamp);
    if (indexToDelete !== -1) {
      this.state.splice(indexToDelete, 1);
    }
  },
  addNotification(notification) {
    if (typeof notification === "string" || notification instanceof String) {
      notification = { message: notification };
    }
    notification.timestamp = new Date();
    notification.timestamp.setMilliseconds(
      notification.timestamp.getMilliseconds() + this.state.length
    );
    notification = Object.assign({}, this.settings, notification);
    this.state.push(notification);
  },
  notify(notification) {
    if (Array.isArray(notification)) {
      notification.forEach(notificationInstance => {
        this.addNotification(notificationInstance);
      });
    } else {
      this.addNotification(notification);
    }
  }
};

const NotificationsPlugin = {
  install(Vue, options) {
    let app = new Vue({
      data: {
        notificationStore: NotificationStore
      },
      methods: {
        notify(notification) {
          this.notificationStore.notify(notification);
        },
        notifyVue: function(
          message,
          verticalAlign,
          horizontalAlign,
          type,
          timeout
        ) {
          this.$notify({
            message: message,
            // component: NotificationTemplateVue,
            icon: "tim-icons icon-bell-55",
            horizontalAlign: horizontalAlign,
            verticalAlign: verticalAlign,
            type: type,
            timeout: timeout
          });
        }
      }
    });
    Vue.prototype.$notify = app.notify;
    Vue.prototype.$notifyVue = app.notifyVue;
    Vue.prototype.$notifications = app.notificationStore;
    Vue.component("Notifications", Notifications);
    if (options) {
      NotificationStore.setOptions(options);
    }
  }
};

export default NotificationsPlugin;
