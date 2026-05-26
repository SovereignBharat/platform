"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Cpu, Database, Globe, Activity, TrendingUp, TrendingDown, Server,
  Shield, Zap, Clock, ArrowUpRight, ArrowDownRight
} from "lucide-react"

const metrics = [
  { title: "Active Deployments", value: "47", change: "+12%", trend: "up", icon: Server },
  { title: "GPU Utilization", value: "78%", change: "+5%", trend: "up", icon: Cpu },
  { title: "API Requests", value: "2.4M", change: "+18%", trend: "up", icon: Globe },
  { title: "Model Inferences", value: "1.2M", change: "-3%", trend: "down", icon: Activity },
]

const deployments = [
  { name: "BharatLLM-7B", status: "running", replicas: 3, gpu: "A100", region: "Mumbai" },
  { name: "IndicBERT-3B", status: "running", replicas: 2, gpu: "A100", region: "Delhi" },
  { name: "VectraDB-Embedding", status: "running", replicas: 5, gpu: "T4", region: "Hyderabad" },
  { name: "SentinelAI-Security", status: "scaling", replicas: 4, gpu: "A100", region: "Bangalore" },
]

const recentActivity = [
  { action: "Model deployed", target: "BharatLLM-13B", time: "2 min ago", user: "admin@sovereignbharat.in" },
  { action: "GPU cluster scaled", target: "cluster-mumbai-01", time: "15 min ago", user: "system" },
  { action: "Policy updated", target: "RBAC-default", time: "1 hour ago", user: "security-team" },
  { action: "New API key created", target: "prod-api-key", time: "2 hours ago", user: "dev@startup.io" },
]

const clusters = [
  { name: "mumbai-prod", status: "healthy", nodes: 12, gpuCount: 24, utilization: 72 },
  { name: "delhi-prod", status: "healthy", nodes: 8, gpuCount: 16, utilization: 85 },
  { name: "hyderabad-prod", status: "healthy", nodes: 6, gpuCount: 12, utilization: 68 },
]

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Platform Overview</h1>
        <p className="text-muted-foreground">India's sovereign cloud and AI infrastructure</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric) => (
          <Card key={metric.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
              <metric.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.value}</div>
              <p className="text-xs text-muted-foreground flex items-center gap-1 mt-1">
                {metric.trend === "up" ? (
                  <TrendingUp className="h-3 w-3 text-green-500" />
                ) : (
                  <TrendingDown className="h-3 w-3 text-red-500" />
                )}
                <span className={metric.trend === "up" ? "text-green-500" : "text-red-500"}>
                  {metric.change}
                </span>
                from last week
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="deployments" className="space-y-4">
        <TabsList>
          <TabsTrigger value="deployments">Active Deployments</TabsTrigger>
          <TabsTrigger value="clusters">Clusters</TabsTrigger>
          <TabsTrigger value="activity">Recent Activity</TabsTrigger>
        </TabsList>

        <TabsContent value="deployments" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>AI Model Deployments</CardTitle>
              <CardDescription>Currently running inference workloads</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {deployments.map((deployment) => (
                  <div key={deployment.name} className="flex items-center justify-between p-4 rounded-lg border">
                    <div className="flex items-center gap-4">
                      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                        <Cpu className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <p className="font-medium">{deployment.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {deployment.replicas} replicas • {deployment.gpu} • {deployment.region}
                        </p>
                      </div>
                    </div>
                    <Badge variant={deployment.status === "running" ? "success" : "warning"}>
                      {deployment.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="clusters" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {clusters.map((cluster) => (
              <Card key={cluster.name}>
                <CardHeader className="flex flex-row items-center justify-between">
                  <CardTitle className="text-sm">{cluster.name}</CardTitle>
                  <Badge variant="success">{cluster.status}</Badge>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-muted-foreground">Nodes</p>
                      <p className="text-xl font-semibold">{cluster.nodes}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">GPUs</p>
                      <p className="text-xl font-semibold">{cluster.gpuCount}</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Utilization</span>
                      <span className="font-medium">{cluster.utilization}%</span>
                    </div>
                    <Progress value={cluster.utilization} />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="activity" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>Platform events and changes</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start gap-4">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted">
                      {activity.action.includes("deploy") ? (
                        <ArrowUpRight className="h-4 w-4 text-green-500" />
                      ) : activity.action.includes("scale") ? (
                        <Zap className="h-4 w-4 text-blue-500" />
                      ) : activity.action.includes("policy") ? (
                        <Shield className="h-4 w-4 text-purple-500" />
                      ) : (
                        <Clock className="h-4 w-4 text-muted-foreground" />
                      )}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">{activity.action}</p>
                      <p className="text-sm text-muted-foreground">{activity.target}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {activity.time} • {activity.user}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" />
              Storage Overview
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Object Storage</span>
                <span className="font-medium">2.4 TB / 10 TB</span>
              </div>
              <Progress value={24} />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Block Storage</span>
                <span className="font-medium">8.7 TB / 20 TB</span>
              </div>
              <Progress value={43} />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Vector Storage</span>
                <span className="font-medium">1.2 TB / 5 TB</span>
              </div>
              <Progress value={24} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Security Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center gap-3 p-3 rounded-lg border">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100">
                  <Shield className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium">All Systems</p>
                  <p className="text-xs text-muted-foreground">Operational</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 rounded-lg border">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
                  <Activity className="h-4 w-4 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium">24h Uptime</p>
                  <p className="text-xs text-muted-foreground">99.9% SLA</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
