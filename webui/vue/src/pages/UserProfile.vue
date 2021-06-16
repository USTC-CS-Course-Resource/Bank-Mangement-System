<template>
  <div class="content">
    <div class="row"></div>
    <div class="col-md-12">
      <a-tabs default-active-key="1" @change="callback">
        <a-tab-pane key="1" tab="Edit">
          <div class="row">
            <div class="col-md-8">
              <edit-profile-form :model="model"> </edit-profile-form>
            </div>
            <div class="col-md-4">
              <user-card :user="user" :model="model"></user-card>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="2" tab="Search" force-render>
          <div class="row">
            <div class="col-md-8">
              <edit-profile-form :model="model"> </edit-profile-form>
            </div>
            <div class="col-md-4">
              <user-card :user="user" :model="model"></user-card>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>
<script>
import EditProfileForm from "./Profile/EditProfileForm.vue";
import UserCard from "./Profile/UserCard.vue";

export default {
  components: {
    EditProfileForm,
    UserCard
  },
  data() {
    return {
      model: {
        cus_id: "350500200001011111",
        cus_name: "小憨憨",
        cus_phone: "123456",
        cus_address: "憨憨家",
        con_name: "小珑珑",
        con_phone: "181111",
        con_email: "666@hanhan.com",
        con_relation: "情侣"
      },
      user: {
        fullName: "Mike Andrew",
        title: "Customer",
        description: ``
      },
      key: "1"
    };
  },
  methods: {
    callback(key) {
      console.log(key);
    }
  }
};
</script>
<style></style>
