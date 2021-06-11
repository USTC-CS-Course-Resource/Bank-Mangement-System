<template>
  <div class="content">
    <!--------------------------- Loan Modal --------------------------->
    <div class="col-md-4">
      <modal
        :show.sync="modals.loanModal"
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
              <small>Loan Pay Records</small>
            </div>
            <div class="table-responsive text-left">
              <search-results-table
                v-on:searchResultsTableHandle="searchResultsTableHandle"
                :data="tableData"
                :columns="tableColumns"
                thead-classes="text-primary"
              >
              </search-results-table>
            </div>
            <div class="text-center">
              <base-button
                type="default"
                class="my-4"
                @click="modals.loanModal = false"
                >OK</base-button
              >
            </div>
          </template>
        </card>
      </modal>
    </div>
    <!--------------------------------------------------------------------------->
    <div class="col-md-12">
      <a-tabs default-active-key="InsertTab" v-model="activeKey">
        <a-tab-pane key="InsertTab" tab="Insert Loan">
          <div class="row">
            <div class="col-md-12">
              <insert-loan :model="insertModel"> </insert-loan>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="SearchTab" tab="Search Loan" force-render>
          <div class="row">
            <div class="col-md-12">
              <search-loan
                v-on:searchResultsTableHandle="searchResultsTableHandle"
                :model="searchModel"
                :shouldReSearch="shouldReSearch"
              >
              </search-loan>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <card>
                <template slot="header">
                  <h4 class="card-title">Search Results</h4>
                </template>
                <div class="table-responsive text-left">
                  <search-results-table
                    v-on:searchResultsTableHandle="searchResultsTableHandle"
                    :data="tableData"
                    :columns="tableColumns"
                    thead-classes="text-primary"
                  >
                  </search-results-table>
                </div>
              </card>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="PayLoanTab" tab="Pay Loan" disabled>
          <div class="row">
            <div class="col-md-12">
              <pay-loan
                :model="payLoanModel"
                v-on:searchResultsTableHandle="searchResultsTableHandle"
              >
              </pay-loan>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <card>
                <template slot="header">
                  <h4 class="card-title">Pay Loan Records</h4>
                </template>
                <div class="table-responsive text-left">
                  <pay-loan-table
                    v-on:searchResultsTableHandle="searchResultsTableHandle"
                    :data="payLoanTableData"
                    :columns="payLoanTableColumns"
                    thead-classes="text-primary"
                  >
                  </pay-loan-table>
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
import { Card } from "@/components/index";
import BaseButton from "@/components/BaseButton";
import Modal from "@/components/Modal";
import InsertLoan from "./Loan/InsertLoan.vue";
import SearchLoan from "./Loan/SearchLoan.vue";
import PayLoan from "./Loan/PayLoan.vue";
import SearchResultsTable from "./Loan/SearchResultsTable.vue";
import PayLoanTable from "./Loan/PayLoanTable.vue";

const tableColumns = ["loa_id", "bra_name", "loa_amount", "actions"];
const payLoanTableColumns = ["loa_pay_id", "loa_pay_amount", "loa_pay_date"];

export default {
  components: {
    Card,
    BaseButton,
    Modal,
    InsertLoan,
    SearchLoan,
    PayLoan,
    SearchResultsTable,
    PayLoanTable
  },
  data() {
    return {
      insertModel: {
        cus_ids: ["350500200001011111"],
        bra_name: "憨憨银行合肥分行"
      },
      searchModel: {
        cus_id: ["350500200001011111"],
        bra_name: "憨憨银行合肥分行"
      },
      payLoanModel: {
        payLoanRecords: []
      },
      tableColumns: tableColumns,
      tableData: [],
      payLoanTableColumns: payLoanTableColumns,
      payLoanTableData: [],
      activeKey: "SearchTab",
      editLoanModel: {},
      modals: {
        loanModal: false
      },
      loanModalData: {
        acc_id: "xxxxxxxxxxxxxxxx",
        acc_balance: 0
      },
      shouldReSearch: 0
    };
  },
  computed: {
    isModalCHECK: function() {
      return this.loanModalData.acc_type == "CHECK";
    }
  },
  methods: {
    searchResultsTableHandle(event) {
      if (event.type == "updateResults") {
        console.log(event.data);
        this.tableData = event.data;
      } else if (event.type == "showPayRecords") {
        this.showPayRecords(event.data);
      }
    },
    showPayRecords(item) {
      axios
        .post("http://localhost:5000/loan/get_pay_loa_records", item)
        .then(response => {
          this.payLoanModel = { payLoanRecords: response.data, ...item };
          console.log("showPayRecords");
          console.log(this.payLoanModel);
          this.payLoanTableData = response.data;
          this.activeKey = "PayLoanTab";
        })
        .catch(error => {
          this.$notifyVue(
            `Get Details Failed! (${error.response.data})`,
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
