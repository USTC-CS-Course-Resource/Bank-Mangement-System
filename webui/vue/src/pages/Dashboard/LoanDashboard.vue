<template>
  <div class="content">
    <!-- Title -->
    <div class="row">
      <div class="col-md-12">
        <card>
          <template slot="header">
            <h4 class="card-title">
              Loan Summary
              <button
                aria-label="Refresh"
                class="dropdown-toggle btn-rotate btn btn-link btn-icon"
                fill
                @click="updateLoanTable"
              >
                <i class="tim-icons icon-refresh-01"></i>
              </button>
            </h4>
          </template>
        </card>
      </div>
    </div>
    <!-- Loan Summary Table -->
    <div class="row">
      <div class="col-md-12">
        <card>
          <div class="text-left" style="height:300px; overflow-y:auto;">
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
    <!-- Loan Summary Chart -->
    <div class="row">
      <!-- LoaAmount Line Chart -->
      <div class="col-lg-6">
        <card type="chart" cardCol>
          <template slot="header">
            <h3 class="card-title">
              <i class="tim-icons icon-money-coins text-success"></i>
              Loan Amount Chart
            </h3>
          </template>
          <bar-chart
            class="chart-area"
            chart-id="loaAmount-bar-chart"
            :chart-data="loaAmountBarChart.chartData"
            :gradient-stops="loaAmountBarChart.gradientStops"
            :extra-options="loaAmountBarChart.extraOptions"
          >
          </bar-chart>
        </card>
      </div>
      <!-- Customer Count Line Chart -->
      <div class="col-lg-6">
        <card type="chart" cardCol>
          <template slot="header">
            <h3 class="card-title">
              <i class="tim-icons icon-single-02 text-info"></i>
              Customer Count
            </h3>
          </template>
          <bar-chart
            class="chart-area"
            chart-id="cus-count-bar-chart"
            :chart-data="cusCountBarChart.chartData"
            :gradient-stops="cusCountBarChart.gradientStops"
            :extra-options="cusCountBarChart.extraOptions"
          >
          </bar-chart>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { Card, BaseInput } from "@/components/index";

import * as chartConfigs from "@/components/Charts/config";
import config from "@/config";
import BarChart from "@/components/Charts/BarChart";
import LoanTable from "./LoanTable";

export default {
  components: {
    Card,
    BarChart,
    BaseInput,
    LoanTable
  },
  data() {
    return {
      bra_name: "憨憨银行合肥分行",
      loanTableColumns: ["bra_name", "date", "loa_amount", "cus_count"],
      time_cycle: "month",
      rawLoanData: []
    };
  },
  computed: {
    loanTableData() {
      var tmp;
      let loanData = this.rawLoanData.filter(
        item => item.bra_name == this.bra_name
      );
      if (this.time_cycle == "month") {
        tmp = loanData;
      } else if (this.time_cycle == "season") {
        tmp = loanData.filter(item => Number(item.date.substr(-5, 2)) % 3 == 0);
        let lastOne = loanData.slice(-1)[0];
        if (lastOne.date && Number(lastOne.date.substr(-5, 2)) % 3 != 0) {
          tmp.push(lastOne);
        }
      } else if (this.time_cycle == "year") {
        tmp = loanData.filter(item => item.date.substr(-5, 2) == "01");
        let lastOne = loanData.slice(-1)[0];
        if (lastOne.date && lastOne.date.substr(-5, 2) != "01") {
          tmp.push(lastOne);
        }
      } else {
        tmp = loanData;
      }
      console.log(tmp);
      return tmp;
    },
    bra_names() {
      return Array.from(new Set(this.rawLoanData.map(item => item.bra_name)));
    },
    loaAmountBarChartLabels() {
      return this.loanTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.date);
    },
    loaAmountBarChartData() {
      return this.loanTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.loa_amount);
    },
    loaAmountBarChart() {
      let loaAmountBarChartConfig = JSON.parse(
        JSON.stringify(chartConfigs.greenBarChartOptions)
      );
      loaAmountBarChartConfig.scales.yAxes[0].ticks = {
        suggestedMin: 0,
        suggestedMax: Math.max(this.cusCountBarChartData),
        padding: 1,
        fontColor: "#9a9a9a"
      };
      return {
        extraOptions: loaAmountBarChartConfig,
        chartData: {
          labels: this.loaAmountBarChartLabels,
          datasets: [
            {
              label: "Date",
              fill: true,
              borderColor: config.colors.primary,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              data: this.loaAmountBarChartData
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0]
      };
    },
    cusCountBarChartLabels() {
      return this.loanTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.date);
    },
    cusCountBarChartData() {
      return this.loanTableData
        .filter(item => item.bra_name == this.bra_name)
        .map(item => item.cus_count);
    },
    cusCountBarChart() {
      let cusCountBarChartConfig = JSON.parse(
        JSON.stringify(chartConfigs.blueBarChartOptions)
      );
      cusCountBarChartConfig.scales.yAxes[0].ticks = {
        suggestedMin: 0,
        suggestedMax: 5,
        padding: 1,
        fontColor: "#9e9e9e"
      };
      return {
        extraOptions: cusCountBarChartConfig,
        chartData: {
          labels: this.cusCountBarChartLabels,
          datasets: [
            {
              label: "Date",
              fill: true,
              borderColor: config.colors.info,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              data: this.cusCountBarChartData
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0]
      };
    }
  },
  methods: {
    updateLoanTable() {
      axios
        .get("http://localhost:5000/loan/get_loan_summary")
        .then(response => {
          this.$notifyVue(`Got Loan Summary`, "top", "center", "success", 2000);
          console.log(response.data);
          this.rawLoanData = response.data;
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
    this.updateLoanTable();
  }
};
</script>
<style></style>
