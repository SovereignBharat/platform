"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import {
  Server, Plus, Play, Pause, Trash2, RefreshCw, ExternalLink,
  Calendar, Clock, HardDrive, Cpu, Globe, Activity
} from "lucide-react"

const deployments = [
  { id: 1, name: "api-gateway-prod", type: "API Gateway", status: "running", replicas: 3, region: "Mumbai", created: "2024-01-15" },
  { id: 2, name: "llm-inference-v2", type: "AI Inference", status: "running", replicas: 4, region: "Delhi", created: "2024-01-18" },
  { id: 3, name: "data-pipeline", type: "Data Pipeline", status: "running", replicas: 2, region: "Hyderabad", created: "2024-01-20" },
  { id: 4, name: "auth-service", type: "Authentication", status: "running", replicas: 3, region: "Bangalore", created: "2024-01-22" },
  { id: 5, name: "model-registry", type: "Model Registry", status: "scaling", replicas: 2, region: "Mumbai", created: "2024-01-25" },
]

export default function DeploymentsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Deployments</h1>
          <p className="text-muted-foreground">Manage your application deployments across regions</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Deployment
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Deployments</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">47</div>
            <p className="text-xs text-muted-foreground">Across all regions</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Running</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">42</div>
            <p className="text-xs text-muted-foreground">Active instances</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Scaling</CardTitle>
            <RefreshCw className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
            <p className="text-xs text-muted-foreground">In progress</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Replicas</CardTitle>
            <Cpu className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">156</div>
            <p className="text-xs text-muted-foreground">Across all deployments</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>All Deployments</CardTitle>
              <CardDescription>View and manage your deployments</CardDescription>
            </div>
            <div className="flex gap-2">
              <Input placeholder="Search deployments..." className="w-64" />
              <Button variant="outline">
                <RefreshCw className="mr-2 h-4 w-4" />
                Refresh
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="grid grid-cols-6 gap-4 border-b pb-3 text-sm font-medium text-muted-foreground">
              <div>Name</div>
              <div>Type</div>
              <div>Status</div>
              <div>Replicas</div>
              <div>Region</div>
              <div>Actions</div>
            </div>
            {deployments.map((deployment) => (
              <div key={deployment.id} className="grid grid-cols-6 gap-4 items-center py-4 border-b last:border-0">
                <div className="flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-muted">
                    <Server className="h-4 w-4" />
                  </div>
                  <span className="font-medium">{deployment.name}</span>
                </div>
                <div>
                  <Badge variant="secondary">{deployment.type}</Badge>
                </div>
                <div>
                  <Badge variant={deployment.status === "running" ? "success" : "warning"}>
                    {deployment.status}
                  </Badge>
                </div>
                <div>
                  <span className="text-sm">{deployment.replicas}</span>
                </div>
                <div>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Globe className="h-3 w-3" />
                    {deployment.region}
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="icon">
                    <Play className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon">
                    <Pause className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon">
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon">
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
