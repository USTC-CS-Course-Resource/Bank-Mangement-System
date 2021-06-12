<template>
  <div class="content">
    <!--------------------------- Account Modal --------------------------->
    <div class="col-md-4">
      <modal
        :show.sync="modals.accountModal"
        body-classes="p-0"
        modal-classes="modal-dialog-centered modal-sm"
      >
        <card
          type="secondary"
          header-classes="bg-white pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0 mb-0"
        >
          <template>
            <div class="text-center text-muted mb-4">
              <small>Update account</small>
            </div>
            <div class="row">
              <div class="col-md-6 pr-md-1 text-left">
                <base-input
                  label="Account ID"
                  v-model="accountModalData.acc_id"
                  placeholder="Account ID"
                  disabled
                >
                </base-input>
              </div>
              <div class="col-md-3 pr-md-1 text-left">
                <base-input
                  label="Type"
                  v-model="accountModalData.acc_type"
                  placeholder="Account ID"
                  disabled
                >
                </base-input>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 pr-md-1 text-left">
                <base-input
                  label="Account Balance"
                  type="Number"
                  v-model="accountModalData.acc_balance"
                  placeholder="balance"
                >
                </base-input>
              </div>
            </div>
            <div class="row" v-if="isModalCHECK">
              <div class="col-md-6 pr-md-1 text-left">
                <base-input
                  label="Overdraft"
                  v-model="accountModalData.che_overdraft"
                  placeholder="overdraft"
                >
                </base-input>
              </div>
            </div>
            <div class="row" v-else>
              <div class="col-md-6 pr-md-1 text-left">
                <base-input
                  label="Interest Rate"
                  placeholder="0.02"
                  v-model="accountModalData.sto_interest_rate"
                >
                </base-input>
              </div>
              <div class="col-md-4 text-left">
                <base-input label="Account Type">
                  <select
                    label="Currency Type"
                    class="form-control"
                    v-model="accountModalData.sto_currency_type"
                  >
                    <option selected>CNY</option>
                    <option>USD</option>
                  </select>
                </base-input>
              </div>
            </div>
            <div class="text-center">
              <base-button type="primary" class="my-4" @click="updateAccount"
                >Save</base-button
              >
              <base-button
                type="default"
                class="my-4"
                @click="modals.accountModal = false"
                >cancel</base-button
              >
            </div>
          </template>
        </card>
      </modal>
    </div>
    <!--------------------------------------------------------------------------->
    <div class="col-md-12">
      <a-tabs default-active-key="SearchTab" v-model="activeKey">
        <a-tab-pane key="OpenTab" tab="Open Account">
          <div class="row">
            <div class="col-md-8">
              <open-account :model="model"> </open-account>
            </div>
            <div class="col-md-4">
              <account-card :card="card" :model="model"></account-card>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="SearchTab" tab="Search Account" force-render>
          <div class="row">
            <div class="col-md-12">
              <search-account
                v-on:searchResultsTableHandle="searchResultsTableHandle"
                :model="searchModel"
                :shouldReSearch="shouldReSearch"
              >
              </search-account>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <card>
                <template slot="header">
                  <h4 class="card-title">Search Results(Store)</h4>
                </template>
                <div class="table-responsive text-left">
                  <store-table
                    v-on:searchResultsTableHandle="searchResultsTableHandle"
                    :data="storeTableData"
                    :columns="storeTableColumns"
                    thead-classes="text-primary"
                  >
                  </store-table>
                </div>
              </card>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <card>
                <template slot="header">
                  <h4 class="card-title">Search Results(Check)</h4>
                </template>
                <div class="table-responsive text-left">
                  <check-table
                    v-on:searchResultsTableHandle="searchResultsTableHandle"
                    :data="checkTableData"
                    :columns="checkTableColumns"
                    thead-classes="text-primary"
                  >
                  </check-table>
                </div>
              </card>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { Card, BaseInput } from "@/components/index";
import BaseButton from "@/components/BaseButton";
import Modal from "@/components/Modal";
import OpenAccount from "./Account/OpenAccount.vue";
import SearchAccount from "./Account/SearchAccount.vue";
import AccountCard from "./Account/AccountCard.vue";
import SearchResultsTable from "./Account/SearchResultsTable.vue";

const storeTableColumns = [
  "acc_id",
  "bra_name",
  "cus_id",
  "acc_type",
  "acc_balance",
  "sto_interest_rate",
  "sto_currency_type",
  "sto_last_visit_date",
  "actions"
];

const checkTableColumns = [
  "acc_id",
  "bra_name",
  "cus_id",
  "acc_type",
  "acc_balance",
  "che_overdraft",
  "che_last_visit_date",
  "actions"
];

export default {
  components: {
    Card,
    BaseInput,
    BaseButton,
    Modal,
    OpenAccount,
    SearchAccount,
    AccountCard,
    storeTable: SearchResultsTable,
    checkTable: SearchResultsTable
  },
  data() {
    return {
      model: {
        acc_id: "0000000000000000",
        cus_id: "350500200001011111",
        bra_name: "憨憨银行合肥分行",
        sto_interest_rate: 0.02,
        sto_currency_type: "CNY"
      },
      searchModel: {
        acc_id: "0000000000000000"
      },
      card: {
        bra_name: "憨憨银行合肥分行",
        title: "高级憨卡",
        description: ``
      },
      search_results: {
        type: Object,
        default: () => {
          return {};
        }
      },
      tableData: [],
      checkTableColumns: checkTableColumns,
      storeTableColumns: storeTableColumns,
      checkTableData: [],
      storeTableData: [],
      tableColumns: storeTableColumns,
      activeKey: "SearchTab",
      editAccountModel: {},
      modals: {
        accountModal: false
      },
      accountModalData: {
        acc_id: "xxxxxxxxxxxxxxxx",
        acc_balance: 0
      },
      modalType: "CHECK",
      shouldReSearch: 0
    };
  },
  computed: {
    accountType: function() {
      return this.model.acc_type;
    },
    isModalCHECK: function() {
      return this.accountModalData.acc_type == "CHECK";
    }
  },
  methods: {
    searchResultsTableHandle(event) {
      if (event.type == "updateResults") {
        console.log(event.data);
        this.storeTableData = event.data["STORE"];
        this.checkTableData = event.data["CHECK"];
      } else if (event.type == "updateStoreResults") {
        this.storeTableData = event.data["STORE"];
      } else if (event.type == "updateCheckResults") {
        this.storeTableData = event.data["CHECK"];
      } else if (event.type == "showStoreAccountModal") {
        this.accountModalData = event.data;
        console.log("showStoreAccountModal");
        console.log(this.accountModalData);
        this.modals.accountModal = true;
      }
    },
    updateAccount() {
      axios
        .post(
          "http://localhost:5000/account/update_account",
          this.accountModalData
        )
        .then(() => {
          this.$notifyVue(`Update Succeed!`, "top", "center", "success", 2000);
          console.log("updateAccount");
          this.tableData.splice(this.accountModalData.index, 1);
          this.tableData = [...this.tableData, this.accountModalData];
          this.shouldReSearch += 1;
          console.log(`shouldReSearch: ${this.shouldReSearch}`);
          console.log(this.tableData);
          this.modals.accountModal = false;
        })
        .catch(error => {
          this.$notifyVue(
            `Update Failed! (${error.response.data})`,
            "top",
            "center",
            "danger",
            2000
          );
        });
    }
  }
};
</script>
<style></style>
