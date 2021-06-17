<template>
  <div class="content">
    <!-- Title -->
    <div class="row">
      <div class="col-md-12">
        <card>
          <template slot="header">
            <h4 class="card-title">
              Account Summary
              <button
                aria-label="Refresh"
                class="dropdown-toggle btn-rotate btn btn-link btn-icon"
                fill
                @click="updateAccountTable"
              >
                <i class="tim-icons icon-refresh-01"></i>
              </button>
            </h4>
          </template>
        </card>
      </div>
    </div>
    <!-- Account Summary Table -->
    <div class="row">
      <div class="col-md-12">
        <card>
          <div class="text-left" style="height:300px; overflow-y:auto;">
            <account-table
              :data="accountTableData"
              :columns="accountTableColumns"
              thead-classes="text-primary"
            >
            </account-table>
          </div>
        </card>
      </div>
    </div>
    <!-- Chart Option -->
    <div class="row">
      <div class="col-md-12">
        <card>
          <template>
            <div class="row">
              <div class="col-md-3 pr-md-1 text-left">
                <base-input label="Branch Name">
                  <select class="form-control" v-model="bra_name">
                    <option
                      v-for="(bra_name_item, index) in bra_names"
                      :key="index"
                      >{{ bra_name_item }}</option
                    >
                  </select>
                </base-input>
              </div>
              <div class="col-md-3 pr-md-1 text-left">
                <base-input label="Time Cycle">
                  <select class="form-control" v-model="time_cycle">
                    <option>month</option>
                    <option>season</option>
                    <option>year</option>
                  </select>
                </base-input>
              </div>
            </div>
          </template>
        </card>
      </div>
    </div>
    <!-- Account Summary Chart -->
    <div class="row">
      <!-- Balance Line Chart -->
      <div class="col-lg-6">
        <card type="chart" cardCol>
          <template slot="header">
            <h3 class="card-title">
              <i class="tim-icons icon-money-coins text-success"></i>
              Balance Chart
            </h3>
          </template>
          <line-chart
            class="chart-area"
            chart-id="balance-line-chart"
            :chart-data="balanceLineChart.chartData"
            :gradient-colors="balanceLineChart.gradientColors"
            :gradient-stops="balanceLineChart.gradientStops"
            :extra-options="balanceLineChart.extraOptions"
          >
          </line-chart>
        </card>
      </div>
      <!-- Customer Count Line Chart -->
      <div class="col-lg-6">
        <card type="chart" cardCol>
          <template slot="header">
            <h3 class="card-title">
              <i class="tim-icons icon-single-02 text-primary"></i>
              Customer Count
            </h3>
          </template>
          <line-chart
            class="chart-area"
            chart-id="cus-count-line-chart"
            :chart-data="cusCountLineChart.chartData"
            :gradient-colors="cusCountLineChart.gradientColors"
            :gradient-stops="cusCountLineChart.gradientStops"
            :extra-options="cusCountLineChart.extraOptions"
          >
          </line-chart>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { Card, BaseInput } from "@/components/index";

import LineChart from "@/components/Charts/LineChart";
import * as chartConfigs from "@/components/Charts/config";
import config from "@/config";
import AccountTable from "./AccountTable";

export default {
  components: {
    Card,
    BaseInput,
    LineChart,
    AccountTable
  },
  data() {
    return {
      bra_name: "憨憨银行合肥分行",
      accountTableColumns: ["bra_name", "date", "balance", "cus_count"],
      time_cycle: "month",
      rawAccountData: []
    };
  },
  computed: {
    accountTableData() {
      var tmp;
      let accountData = this.rawAccountData.filter(
        item => item.bra_name == this.bra_name
      );
      if (this.time_cycle == "month") {
        tmp = accountData;
      } else if (this.time_cycle == "season") {
        const month2season = {
          "01": "S1",
          "02": "S1",
          "03": "S1",
          "04": "S2",
          "05": "S2",
          "06": "S2",
          "07": "S3",
          "08": "S3",
          "09": "S3",
          "10": "S4",
          "11": "S4",
          "12": "S4"
        };
        tmp = accountData.filter(
          item => Number(item.date.substr(-5, 2)) % 3 == 0
        );
        let lastOne = accountData.slice(-1)[0];
        if (lastOne.date && Number(lastOne.date.substr(-5, 2)) % 3 != 0) {
          tmp.push(lastOne);
        }
        tmp = tmp.map(item => {
          return {
            ...item,
            date: item.date.slice(0, 5) + month2season[item.date.substr(-5, 2)]
          };
        });
      } else if (this.time_cycle == "year") {
        tmp = accountData.filter(item => item.date.substr(-5, 2) == "01");
        let lastOne = accountData.slice(-1)[0];
        if (lastOne.date && lastOne.date.substr(-5, 2) != "01") {
          tmp.push(lastOne);
        }
        tmp = tmp.map(item => {
          return { ...item, date: item.date.slice(0, 4) };
        });
      } else {
        tmp = accountData;
      }
      console.log(tmp);
      return tmp;
    },
    bra_names() {
      return Array.from(
        new Set(this.rawAccountData.map(item => item.bra_name))
      );
    },
    balanceLineChartLabels() {
      return this.accountTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.date);
    },
    balanceLineChartData() {
      return this.accountTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.balance);
    },
    balanceLineChart() {
      let balanceLineChartConfig = JSON.parse(
        JSON.stringify(chartConfigs.greenChartOptions)
      );
      balanceLineChartConfig.scales.yAxes[0].ticks = {
        suggestedMin: 0,
        suggestedMax: Math.max(this.cusCountLineChartData),
        padding: 1,
        fontColor: "#9a9a9a"
      };
      return {
        extraOptions: balanceLineChartConfig,
        chartData: {
          labels: this.balanceLineChartLabels,
          datasets: [
            {
              label: "Balance",
              fill: true,
              borderColor: config.colors.primary,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.primary,
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: config.colors.primary,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: this.balanceLineChartData
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.2, 0]
      };
    },
    cusCountLineChartLabels() {
      return this.accountTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.date);
    },
    cusCountLineChartData() {
      return this.accountTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.cus_count);
    },
    cusCountLineChart() {
      let cusCountLineChartConfig = JSON.parse(
        JSON.stringify(chartConfigs.purpleChartOptions)
      );
      cusCountLineChartConfig.scales.yAxes[0].ticks = {
        suggestedMin: 0,
        suggestedMax: Math.max(this.cusCountLineChartData),
        padding: 1,
        fontColor: "#9a9a9a"
      };
      return {
        extraOptions: cusCountLineChartConfig,
        chartData: {
          labels: this.cusCountLineChartLabels,
          datasets: [
            {
              label: "Customer Count",
              fill: true,
              borderColor: config.colors.danger,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.danger,
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: config.colors.danger,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: this.cusCountLineChartData
            }
          ]
        },
        gradientColors: [
          "rgba(66,134,121,0.15)",
          "rgba(66,134,121,0.0)",
          "rgba(66,134,121,0)"
        ],
        gradientStops: [1, 0.4, 0]
      };
    }
  },
  methods: {
    updateAccountTable() {
      axios
        .post("http://localhost:5000/account/get_account_summary", {
          token: this.$store.state.token
        })
        .then(response => {
          this.$notifyVue(
            `Got Account Summary`,
            "top",
            "center",
            "success",
            2000
          );
          console.log(response.data);
          this.rawAccountData = response.data;
        })
        .catch(error => {
          if (!error.response) {
            console.log(error);
            this.$notify_connection_error(error);
            return;
          }
          this.$notifyVue(
            `Failed to get Summary! (${error.response.data})`,
            "top",
            "center",
            "danger",
            4000
          );
        });
    }
  },
  mounted() {
    this.updateAccountTable();
  }
};
</script>
<style></style>
