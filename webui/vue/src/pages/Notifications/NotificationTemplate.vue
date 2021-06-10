<template>
  <div>{{ notificationContent }}aaa</div>
</template>

<script>
export default {
  name: "notification-template",
  props: {
    notificationContent: {
      type: String,
      default: () => {
        return "default";
      }
    }
  }
};
</script>
