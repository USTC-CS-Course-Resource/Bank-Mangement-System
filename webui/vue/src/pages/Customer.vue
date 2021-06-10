<template>
  <div class="content">
    <div class="row"></div>
    <div class="col-md-12">
      <a-tabs default-active-key="1">
        <a-tab-pane key="1" tab="Insert">
          <div class="row">
            <div class="col-md-8">
              <insert-customer :model="model"> </insert-customer>
            </div>
            <div class="col-md-4">
              <customer-card :cus="cus" :model="model"></customer-card>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="2" tab="Search" force-render>
          <div class="row">
            <div class="col-md-12">
              <search-customer
                v-on:returnResults="returnResults"
                :model="model"
              >
              </search-customer>
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
                    v-on:returnResults="returnResults"
                    :data="table.data"
                    :columns="table.columns"
                    thead-classes="text-primary"
                  >
                  </search-results-table>
                </div>
              </card>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="3" tab="Edit" disabled>
          <div class="row">
            <div class="col-md-8">
              <edit-customer :model="model"> </edit-customer>
            </div>
            <div class="col-md-4">
              <customer-card :cus="cus" :model="model"></customer-card>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>
<script>
import { Card } from "@/components/index";
import InsertCustomer from "./Customer/InsertCustomer.vue";
import EditCustomer from "./Customer/EditCustomer.vue";
import SearchCustomer from "./Customer/SearchCustomer.vue";
import CustomerCard from "./Customer/CustomerCard.vue";
import SearchResultsTable from "./Customer/SearchResultsTable.vue";

const tableColumns = [
  "cus_id",
  "cus_name",
  "cus_phone",
  "cus_address",
  "con_name",
  "con_phone",
  "con_email",
  "con_relation",
  "actions"
];

export default {
  components: {
    Card,
    InsertCustomer,
    EditCustomer,
    SearchCustomer,
    CustomerCard,
    SearchResultsTable
  },
  data() {
    return {
      model: {
        cus_id: "350500200001011111",
        cus_name: "小憨憨",
        cus_phone: "123456",
        cus_address: "憨憨家",
        con_name: "小恐龙",
        con_phone: "181111",
        con_email: "666@hanhan.com",
        con_relation: "情侣"
      },
      cus: {
        fullName: "Mike Andrew",
        title: "Customer",
        description: ``
      },
      search_results: {
        type: Object,
        default: () => {
          return {};
        }
      },
      tableData: []
    };
  },
  computed: {
    table: function() {
      return {
        title: "Search Results",
        columns: [...tableColumns],
        data: [...this.tableData]
      };
    }
  },
  methods: {
    returnResults(results) {
      this.tableData = results;
      console.log(this.tableData);
    }
  }
};
</script>
<style></style>
