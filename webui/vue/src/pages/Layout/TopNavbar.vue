<template>
  <nav
    class="navbar navbar-expand-lg navbar-absolute"
    :class="{ 'bg-white': showMenu, 'navbar-transparent': !showMenu }"
  >
    <div class="container-fluid">
      <div class="navbar-wrapper">
        <div
          class="navbar-toggle d-inline"
          :class="{ toggled: $sidebar.showSidebar }"
        >
          <button type="button" class="navbar-toggler" @click="toggleSidebar">
            <span class="navbar-toggler-bar bar1"></span>
            <span class="navbar-toggler-bar bar2"></span>
            <span class="navbar-toggler-bar bar3"></span>
          </button>
        </div>
        <a class="navbar-brand" href="javascript:void(0)"> {{ $route.name }}</a>
      </div>
      <button
        class="navbar-toggler"
        type="button"
        @click="toggleMenu"
        data-toggle="collapse"
        data-target="#navigation"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
      </button>
      <div class="collapse navbar-collapse show text-left" v-show="showMenu">
        <ul class="navbar-nav" :class="$rtl.isRTL ? 'mr-auto' : 'ml-auto'">
          <!------------------------------------ Initialize whole database ------------------------------------>
          <li class="search-bar input-group" @click="initializeBankDB">
            <button class="btn btn-link" id="initialize-button">
              <i class="tim-icons icon-refresh-01"></i>
              <span class="d-lg-none d-md-block">Initialize</span>
            </button>
          </li>
          <!------------------------------------ Clear BankDB button ------------------------------------>
          <li class="search-bar input-group" @click="clearBankDB">
            <button class="btn btn-link" id="clear-button">
              <i class="tim-icons icon-simple-remove"></i>
              <span class="d-lg-none d-md-block">Clear</span>
            </button>
          </li>
          <!------------------------------------ Search button ------------------------------------>
          <!-- <li class="search-bar input-group" @click="searchModalVisible = true">
            <button
              class="btn btn-link"
              id="search-button"
              data-toggle="modal"
              data-target="#searchModal"
            >
              <i class="tim-icons icon-zoom-split"></i>
              <span class="d-lg-none d-md-block">Search</span>
            </button>
          </li>
          <modal
            :show.sync="searchModalVisible"
            class="modal-search"
            id="searchModal"
            :centered="false"
            :show-close="true"
          >
            <input
              slot="header"
              v-model="searchQuery"
              type="text"
              class="form-control"
              id="inlineFormInputGroup"
              placeholder="SEARCH"
            />
          </modal> -->
          <!------------------------------------ Notification ------------------------------------>
          <!-- <drop-down>
            <a
              href="javascript:void(0)"
              data-toggle="dropdown"
              class="dropdown-toggle nav-link"
            >
              <div class="notification d-none d-lg-block d-xl-block"></div>
              <i class="tim-icons icon-sound-wave"></i>
              <p class="d-lg-none text-left">Notifications</p>
            </a>
            <ul class="dropdown-menu dropdown-menu-right dropdown-navbar">
              <li class="nav-link">
                <a href="#" class="nav-item dropdown-item">notification 1</a>
              </li>
              <li class="nav-link">
                <a href="javascript:void(0)" class="nav-item dropdown-item"
                  >notification 2</a
                >
              </li>
            </ul>
          </drop-down> -->
          <!-- User -->
          <drop-down>
            <a href="#" class="dropdown-toggle nav-link" data-toggle="dropdown">
              <div class="photo">
                <img src="@/assets/img/anime3.png" alt="Profile Photo" />
              </div>
              <b class="caret d-none d-lg-block d-xl-block"></b>
              <p class="d-lg-none">Log out</p>
            </a>
            <ul class="dropdown-menu dropdown-navbar">
              <!-- <li class="nav-link">
                <a href="javascript:void(0)" class="nav-item dropdown-item"
                  >Profile</a
                >
              </li>
              <li class="nav-link">
                <a href="javascript:void(0)" class="nav-item dropdown-item"
                  >Settings</a
                >
              </li>
              <li class="dropdown-divider"></li> -->
              <li class="nav-link">
                <a href="/login" class="nav-item dropdown-item" @click="logout"
                  >Log out</a
                >
              </li>
            </ul>
          </drop-down>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import DropDown from "@/components/Dropdown.vue";
// import Modal from "@/components/Modal.vue";
import axios from "axios";

// import { SidebarPlugin } from "@/components/index";

export default {
  components: {
    DropDown
    // Modal
    // SidebarPlugin
  },
  data() {
    return {
      searchModalVisible: false,
      searchQuery: "",
      showMenu: false
    };
  },
  methods: {
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    logout() {
      this.$store.state.username = null;
      this.$store.state.token = null;
    },
    clearBankDB() {
      axios
        .post("http://localhost:5000/bankdb/clear", {
          token: this.$store.state.token
        })
        .then(() => {
          this.$notifyVue(`Clear All Tables`, "top", "center", "success", 2000);
        })
        .catch(error => {
          if (!error.response) {
            this.$notify_connection_error(error);
          } else {
            console.log(error.response);
            if (
              error.response.data == "LoginExpired" ||
              error.response.data.includes("ExpiredSignatureError")
            ) {
              this.$loginExpiredAction();
            } else {
              this.$notifyVue(
                `Failed to Clear All Tables! (${error.response.data})`,
                "top",
                "center",
                "danger",
                4000
              );
            }
          }
        });
    },
    initializeBankDB() {
      axios
        .post("http://localhost:5000/bankdb/initialize", {
          token: this.$store.state.token
        })
        .then(() => {
          this.$notifyVue(
            `Initialization succeed!`,
            "top",
            "center",
            "success",
            2000
          );
        })
        .catch(error => {
          if (!error.response) {
            this.$notify_connection_error(error);
          } else {
            console.log(error.response);
            if (
              error.response.data == "LoginExpired" ||
              error.response.data.includes("ExpiredSignatureError")
            ) {
              this.$loginExpiredAction();
            } else {
              this.$notifyVue(
                `Initialization Failed! (${error.response.data})`,
                "top",
                "center",
                "danger",
                4000
              );
            }
          }
        });
    }
  },
  computed: {
    isRTL() {
      return this.$rtl.isRTL;
    }
  }
};
</script>
<style></style>
