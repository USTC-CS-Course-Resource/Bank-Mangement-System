import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";
import Login from "@/pages/Login.vue";
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
    children: [
      {
        path: "login",
        name: "Login",
        component: Login
      },
      {
        path: "dashboard",
        name: "Dashboard",
        meta: {
          keepAlive: true,
          requireAuth: true
        },
        component: Dashboard
      },
      {
        path: "customer",
        name: "Customer",
        meta: {
          keepAlive: true,
          requireAuth: true
        },
        component: Customer
      },
      {
        path: "account",
        name: "Account",
        meta: {
          keepAlive: true,
          requireAuth: true
        },
        component: Account
      },
      {
        path: "loan",
        name: "Loan",
        meta: {
          keepAlive: true,
          requireAuth: true
        },
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
