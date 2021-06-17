<template>
  <div class="fixed-plugin" v-click-outside="closeDropDown">
    <div class="dropdown show-dropdown" :class="{ show: isOpen }">
      <a data-toggle="dropdown" class="settings-icon">
        <i class="fa fa-cog fa-2x" @click="toggleDropDown"> </i>
      </a>
      <ul class="dropdown-menu" :class="{ show: isOpen }">
        <li class="header-title">Sidebar Background</li>
        <li class="adjustments-line">
          <a class="switch-trigger background-color">
            <div class="badge-colors text-center">
              <span
                v-for="item in sidebarColors"
                :key="item.color"
                class="badge filter"
                :class="[`badge-${item.color}`, { active: item.active }]"
                :data-color="item.color"
                @click="changeSidebarBackground(item)"
              >
              </span>
            </div>
            <div class="clearfix"></div>
          </a>
        </li>

        <li class="header-title">Welcome to my Github</li>

        <li class="button-container text-center">
          <social-sharing
            url="https://github.com/RabbitWhite1"
            inline-template
            title="Han-Han-Bank Management System"
          >
            <div>
              <h3>
                <a href="https://github.com/RabbitWhite1" target="_blank">
                  <i class="fab fa-github"></i>
                </a>
              </h3>
            </div>
          </social-sharing>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    backgroundColor: String
  },
  data() {
    return {
      isOpen: false,
      sidebarColors: [
        { color: "primary", active: false, value: "primary" },
        { color: "info", active: false, value: "blue" },
        { color: "success", active: false, value: "green" }
      ]
    };
  },
  methods: {
    toggleDropDown() {
      this.isOpen = !this.isOpen;
    },
    closeDropDown() {
      this.isOpen = false;
    },
    toggleList(list, itemToActivate) {
      list.forEach(listItem => {
        listItem.active = false;
      });
      itemToActivate.active = true;
    },
    changeSidebarBackground(item) {
      this.$emit("update:backgroundColor", item.value);
      this.toggleList(this.sidebarColors, item);
    }
  }
};
</script>
<style></style>
