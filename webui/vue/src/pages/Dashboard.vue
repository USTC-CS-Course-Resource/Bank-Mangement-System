<template>
  <div class="content">
    <a-tabs default-active-key="AccountTab" v-model="activeKey">
      <!------------------------------------ Account Summary ------------------------------------>
      <a-tab-pane key="AccountTab" tab="Account Dashboard" force-render>
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
                    :class="isRTL ? 'pl-5 float-left' : ''"
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
                  <div class="col-md-4 pr-md-1 text-left">
                    <base-input
                      label="Branch Name"
                      placeholder="Branch Name"
                      v-model="bra_name"
                    >
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
                  <i class="tim-icons icon-bell-55 text-primary"></i>
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
                  <i class="tim-icons icon-send text-success"></i>
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
      </a-tab-pane>
      <!------------------------------------ Loan Summary ------------------------------------>
      <a-tab-pane key="LoanTab" tab="Loan Dashboard">
        <div class="row">
          <div class="col-md-12">
            <card>
              <template slot="header">
                <h5 class="title">Search Conditions</h5>
              </template>
              <div class="row">
                <div class="col-md-5 text-left">
                  <base-input
                    label="Branch Name"
                    placeholder="憨憨银行合肥分行"
                    v-model="bra_name"
                  >
                  </base-input>
                </div>
              </div>
            </card>
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <card>
              <template slot="header">
                <h4 class="card-title">Loan Table</h4>
              </template>
              <div class="table-responsive text-left">
                <loan-table
                  :data="loanTableData"
                  :columns="loanTableColumns"
                  thead-classes="text-primary"
                >
                </loan-table>
              </div>
            </card>
          </div>
        </div>
      </a-tab-pane>
    </a-tabs>
    <div class="row">
      <div class="col-12">
        <card type="chart">
          <template slot="header">
            <div class="row">
              <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
                <h5 class="card-category">Total Shipments</h5>
                <h2 class="card-title">Performance</h2>
              </div>
              <div class="col-sm-6">
                <div
                  class="btn-group btn-group-toggle"
                  data-toggle="buttons"
                  :class="isRTL ? 'float-left' : 'float-right'"
                >
                  <label
                    v-for="(option, index) in bigLineChartCategories"
                    :key="option"
                    class="btn btn-success btn-sm btn-simple"
                    :class="{ active: bigLineChart.activeIndex === index }"
                    :id="index"
                  >
                    <input
                      type="radio"
                      @click="initBigChart(index)"
                      name="options"
                      autocomplete="off"
                      :checked="bigLineChart.activeIndex === index"
                    />
                    {{ option }}
                  </label>
                </div>
              </div>
            </div>
          </template>
          <line-chart
            class="chart-area"
            ref="bigChart"
            chart-id="big-line-chart"
            :chart-data="bigLineChart.chartData"
            :gradient-colors="bigLineChart.gradientColors"
            :gradient-stops="bigLineChart.gradientStops"
            :extra-options="bigLineChart.extraOptions"
          >
          </line-chart>
        </card>
      </div>
    </div>
    <div class="row">
      <!-- 曲线图 -->
      <div class="col-lg-4" :class="{ 'text-right': isRTL }">
        <card type="chart" cardCol>
          <template slot="header">
            <h5 class="card-category">{{ $t("dashboard.totalShipments") }}</h5>
            <h3 class="card-title">
              <i class="tim-icons icon-bell-55 text-primary"></i> 763,215
            </h3>
          </template>
          <line-chart
            class="chart-area"
            chart-id="green-line-chart"
            :chart-data="greenLineChart.chartData"
            :gradient-colors="greenLineChart.gradientColors"
            :gradient-stops="greenLineChart.gradientStops"
            :extra-options="greenLineChart.extraOptions"
          >
          </line-chart>
        </card>
      </div>
      <!-- 条形图 -->
      <div class="col-lg-4">
        <card type="chart" cardCol>
          <template slot="header">
            <h5 class="card-category">{{ $t("dashboard.dailySales") }}</h5>
            <h3 class="card-title">
              <i class="tim-icons icon-delivery-fast text-info"></i> 3,500€
            </h3>
          </template>
          <bar-chart
            class="chart-area"
            chart-id="blue-bar-chart"
            :chart-data="blueBarChart.chartData"
            :gradient-stops="blueBarChart.gradientStops"
            :extra-options="blueBarChart.extraOptions"
          >
          </bar-chart>
        </card>
      </div>
      <!-- 曲线图 -->
      <div class="col-lg-4">
        <card type="chart" cardCol>
          <template slot="header">
            <h5 class="card-category">{{ $t("dashboard.completedTasks") }}</h5>
            <h3 class="card-title">
              <i class="tim-icons icon-send text-success"></i> 12,100K
            </h3>
          </template>
          <line-chart
            class="chart-area"
            chart-id="purple-line-chart"
            :chart-data="purpleLineChart.chartData"
            :gradient-colors="purpleLineChart.gradientColors"
            :gradient-stops="purpleLineChart.gradientStops"
            :extra-options="purpleLineChart.extraOptions"
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
import BarChart from "@/components/Charts/BarChart";
import * as chartConfigs from "@/components/Charts/config";
import config from "@/config";
import AccountTable from "./Dashboard/AccountTable";
import LoanTable from "./Dashboard/LoanTable";

export default {
  components: {
    Card,
    BaseInput,
    LineChart,
    BarChart,
    AccountTable,
    LoanTable
  },
  data() {
    return {
      activeKey: "AccountTab",
      bra_name: "憨憨银行合肥分行",
      accountTableData: [],
      accountTableColumns: ["bra_name", "date", "balance", "cus_count"],
      loanTableData: [],
      loanTableColumns: [],
      //
      //
      bigLineChartCategories: ["Accounts", "Purchases", "Sessions"],
      bigLineChart: {
        allData: [
          [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
          [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
          [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130]
        ],
        activeIndex: 0,
        chartData: { datasets: [{}] },
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: []
      },
      greenLineChart: {
        extraOptions: chartConfigs.greenChartOptions,
        chartData: {
          labels: ["JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          datasets: [
            {
              label: "Data",
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
              data: [80, 100, 70, 80, 120, 80]
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.2, 0]
      },
      blueBarChart: {
        extraOptions: chartConfigs.barChartOptions,
        chartData: {
          labels: ["USA", "GER", "AUS", "UK", "RO", "BR"],
          datasets: [
            {
              label: "Countries",
              fill: true,
              borderColor: config.colors.info,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              data: [53, 20, 10, 80, 100, 45]
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0]
      },
      purpleLineChart: {
        extraOptions: chartConfigs.purpleChartOptions,
        chartData: {
          labels: ["JUL", "AUG", "SEP", "OCT", "NOV"],
          datasets: [
            {
              label: "My First dataset",
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
              data: [90, 27, 60, 12, 80]
            }
          ]
        },
        gradientColors: [
          "rgba(66,134,121,0.15)",
          "rgba(66,134,121,0.0)",
          "rgba(66,134,121,0)"
        ],
        gradientStops: [1, 0.4, 0]
      }
    };
  },
  computed: {
    enableRTL() {
      return this.$route.query.enableRTL;
    },
    isRTL() {
      return this.$rtl.isRTL;
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
              label: "Data",
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
              label: "My First dataset",
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
        .get("http://localhost:5000/account/get_account_summary")
        .then(response => {
          this.$notifyVue(
            `Got Account Summary`,
            "top",
            "center",
            "success",
            2000
          );
          console.log(response.data);
          this.accountTableData = response.data;
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
    },
    initBigChart(index) {
      let chartData = {
        datasets: [
          {
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
            data: this.bigLineChart.allData[index]
          }
        ],
        labels: [
          "JAN",
          "FEB",
          "MAR",
          "APR",
          "MAY",
          "JUN",
          "JUL",
          "AUG",
          "SEP",
          "OCT",
          "NOV",
          "DEC"
        ]
      };
      this.$refs.bigChart.updateGradients(chartData);
      this.bigLineChart.chartData = chartData;
      this.bigLineChart.activeIndex = index;
    }
  },
  mounted() {
    this.i18n = this.$i18n;
    if (this.enableRTL) {
      this.i18n.locale = "ar";
      this.$rtl.enableRTL();
    }
    this.initBigChart(0);
  },
  beforeDestroy() {
    if (this.$rtl.isRTL) {
      this.i18n.locale = "en";
      this.$rtl.disableRTL();
    }
  }
};
</script>
<style></style>
