<template>
  <div class="wrapper">
    <!-- <div class="wrapper" :class="{'nav-open': $sidebar.showSidebar}"> -->

    <side-bar :background-color="backgroundColor">
      <!-- <mobile-menu slot="content"></mobile-menu> -->
      <sidebar-link to="/dashboard">
        <i class="tim-icons icon-chart-pie-36"></i>
        <template v-if="!isRTL">
          <p>Dashboard</p>
        </template>
        <template v-else>
          <p>控制面板</p>
        </template>
      </sidebar-link>
      <sidebar-link to="/customer">
        <i class="tim-icons icon-single-02"></i>
        <template v-if="!isRTL">
          <p>Customer</p>
        </template>
        <template v-else>
          <p>客户</p>
        </template>
      </sidebar-link>
      <sidebar-link to="/account">
        <i class="tim-icons icon-paper"></i>
        <template v-if="!isRTL">
          <p>Account</p>
        </template>
        <template v-else>
          <p>账户</p>
        </template>
      </sidebar-link>
      <sidebar-link to="/loan">
        <i class="tim-icons icon-coins"></i>
        <template v-if="!isRTL">
          <p>Loan</p>
        </template>
        <template v-else>
          <p>贷款</p>
        </template>
      </sidebar-link>
      <sidebar-link to="/icons">
        <i class="tim-icons icon-atom"></i>
        <template v-if="!isRTL">
          <p>Icons</p>
        </template>
        <template v-else>
          <p>图标</p>
        </template>
      </sidebar-link>
      <!-- <sidebar-link to="/maps">
        <i class="tim-icons icon-pin"></i>
        <template v-if="!isRTL">
          <p>Maps</p>
        </template>
        <template v-else>
          <p>地图</p>
        </template>
      </sidebar-link> -->
      <sidebar-link to="/typography">
        <i class="tim-icons icon-align-center"></i>
        <template v-if="!isRTL">
          <p>Typography</p>
        </template>
        <template v-else>
          <p>排版</p>
        </template>
      </sidebar-link>
    </side-bar>
    <sidebar-share :background-color.sync="backgroundColor"></sidebar-share>

    <div class="main-panel" :data="backgroundColor">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"></dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss"></style>
<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./DashboardContent.vue";
import SidebarShare from "./SidebarSharePlugin.vue";
// import MobileMenu from "./MobileMenu.vue";
import SideBar from "@/components/SidebarPlugin/SideBar.vue";
import SidebarLink from "@/components/SidebarPlugin/SidebarLink.vue";

export default {
  components: {
    TopNavbar,
    DashboardContent,
    ContentFooter,
    // MobileMenu,
    SideBar,
    SidebarLink,
    SidebarShare
  },
  data() {
    return {
      backgroundColor: "green"
    };
  },
  computed: {
    isRTL() {
      return this.$rtl.isRTL;
    }
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    }
  }
};
</script>
