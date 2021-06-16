import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Dashboard from "@/pages/Dashboard.vue";
import Customer from "@/pages/Customer.vue";
import Account from "@/pages/Account.vue";
import Loan from "@/pages/Loan.vue";
import Icons from "@/pages/Icons.vue";
import Maps from "@/pages/Maps.vue";
import Typography from "@/pages/Typography.vue";

const routes = [
  {
    path: "/",
    component: DashboardLayout,
    redirect: "dashboard",
    meta: {
      keepAlive: true
    },
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: Dashboard
      },
      {
        path: "customer",
        name: "Customer",
        component: Customer
      },
      {
        path: "account",
        name: "Account",
        component: Account
      },
      {
        path: "loan",
        name: "Loan",
        component: Loan
      },
      {
        path: "icons",
        name: "Icons",
        component: Icons
      },
      {
        path: "maps",
        name: "Maps",
        component: Maps
      },
      {
        path: "typography",
        name: "Typography",
        component: Typography
      }
    ]
  }
];

export default routes;
