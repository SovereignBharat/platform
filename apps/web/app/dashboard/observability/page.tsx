"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import {
  Activity, Cpu, HardDrive, Network, Server, Clock, AlertTriangle,
  TrendingUp, Zap, MemoryStick
} from "lucide-react"

const metrics = [
  { name: "API Latency", value: "45ms", change: "-12%", status: "healthy" },
  { name: "Request Rate", value: "12.4K/s", change: "+8%", status: "healthy" },
  { name: "Error Rate", value: "0.02%", change: "-5%", status: "healthy" },
  { name: "GPU Memory", value: "67%", change: "+3%", status: "warning" },
]

const services = [
  { name: "Control Plane", status: "healthy", uptime: "99.99%", requests: "1.2M" },
  { name: "Gateway", status: "healthy", uptime: "99.95%", requests: "2.4M" },
  { name: "IAM Service", status: "healthy", uptime: "99.99%", requests: "890K" },
  { name: "Inference Engine", status: "healthy", uptime: "99.90%", requests: "1.1M" },
  { name: "GPU Scheduler", status: "warning", uptime: "99.50%", requests: "450K" },
]

const recentAlerts = [
  { message: "High memory usage on mumbai-prod cluster", severity: "warning", time: "5 min ago" },
  { message: "Inference latency spike detected", severity: "info", time: "15 min ago" },
  { message: "Autoscaling triggered for llm-inference", severity: "info", time: "30 min ago" },
  { message: "GPU pool utilization above threshold", severity: "warning", time: "1 hour ago" },
]

export default function ObservabilityPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Observability</h1>
        <p className="text-muted-foreground">Monitor system health, performance, and alerts</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric) => (
          <Card key={metric.name}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.value}</div>
              <div className="flex items-center gap-2 mt-1">
                <Badge variant={metric.status === "healthy" ? "success" : "warning"}>
                  {metric.status}
                </Badge>
                <span className="text-xs text-muted-foreground">{metric.change} vs last hour</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Server className="h-5 w-5" />
              Service Health
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {services.map((service) => (
                <div key={service.name} className="flex items-center justify-between p-3 rounded-lg border">
                  <div className="flex items-center gap-3">
                    <div className={`h-3 w-3 rounded-full ${service.status === "healthy" ? "bg-green-500" : "bg-amber-500"}`} />
                    <span className="font-medium">{service.name}</span>
                  </div>
                  <div className="flex items-center gap-6 text-sm">
                    <div className="text-right">
                      <p className="text-muted-foreground">Uptime</p>
                      <p className="font-medium">{service.uptime}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-muted-foreground">Requests</p>
                      <p className="font-medium">{service.requests}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Recent Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentAlerts.map((alert, index) => (
                <div key={index} className="flex items-start gap-3 p-3 rounded-lg border">
                  <div className={`mt-0.5 h-2 w-2 rounded-full ${alert.severity === "warning" ? "bg-amber-500" : "bg-blue-500"}`} />
                  <div className="flex-1">
                    <p className="text-sm">{alert.message}</p>
                    <p className="text-xs text-muted-foreground">{alert.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>GPU Resource Utilization</CardTitle>
          <CardDescription>Real-time GPU metrics across clusters</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">A100 Pool</span>
                <span className="font-medium">72%</span>
              </div>
              <Progress value={72} />
              <p className="text-xs text-muted-foreground">18/24 GPUs active</p>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">T4 Pool</span>
                <span className="font-medium">45%</span>
              </div>
              <Progress value={45} />
              <p className="text-xs text-muted-foreground">7/16 GPUs active</p>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">H100 Pool</span>
                <span className="font-medium">38%</span>
              </div>
              <Progress value={38} />
              <p className="text-xs text-muted-foreground">3/8 GPUs active</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
