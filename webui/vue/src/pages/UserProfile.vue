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
        cus_id: "",
        cus_name: "",
        cus_phone: "",
        cus_address: "",
        con_name: "",
        con_phone: "",
        con_email: "",
        con_relation: ""
      },
      user: {
        fullName: "Mike Andrew",
        title: "Ceo/Co-Founder",
        description: `Do not be scared of the truth because we need to restart the human foundation in truth And I love you like Kanye loves Kanye I love Rick Owens’ bed design but the back is...`
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
