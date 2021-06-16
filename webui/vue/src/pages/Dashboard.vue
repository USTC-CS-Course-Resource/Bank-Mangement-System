<template>
  <div class="content">
    <a-tabs default-active-key="AccountTab" v-model="activeKey">
      <!------------------------------------ Account Summary ------------------------------------>
      <a-tab-pane key="AccountTab" tab="Account Dashboard" force-render>
        <account-dashboard></account-dashboard>
      </a-tab-pane>
      <!------------------------------------ Loan Summary ------------------------------------>
      <a-tab-pane key="LoanTab" tab="Loan Dashboard" force-render>
        <loan-dashboard></loan-dashboard>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>
<script>
import AccountDashboard from "./Dashboard/AccountDashboard";
import LoanDashboard from "./Dashboard/LoanDashboard";

export default {
  components: {
    AccountDashboard,
    LoanDashboard
  },
  data() {
    return {
      activeKey: "AccountTab"
    };
  },
  computed: {},
  methods: {}
};
</script>
<style></style>
