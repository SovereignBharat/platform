"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import {
  Server, Plus, Settings, HardDrive, Cpu, Globe, Network,
  RefreshCw, Trash2, Eye
} from "lucide-react"

const clusters = [
  { 
    name: "mumbai-prod-01", 
    region: "Mumbai (West)",
    status: "healthy",
    nodes: 12,
    gpuCount: 24,
    cpuCores: 192,
    memory: "768 GB",
    utilization: 72,
    pods: 156
  },
  { 
    name: "delhi-prod-01", 
    region: "Delhi (North)",
    status: "healthy",
    nodes: 8,
    gpuCount: 16,
    cpuCores: 128,
    memory: "512 GB",
    utilization: 85,
    pods: 98
  },
  { 
    name: "hyderabad-prod-01", 
    region: "Hyderabad (South)",
    status: "healthy",
    nodes: 6,
    gpuCount: 12,
    cpuCores: 96,
    memory: "384 GB",
    utilization: 68,
    pods: 72
  },
]

export default function ClustersPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Kubernetes Clusters</h1>
          <p className="text-muted-foreground">Manage and monitor your Kubernetes infrastructure</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Create Cluster
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Clusters</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">Across India regions</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Nodes</CardTitle>
            <Cpu className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">26</div>
            <p className="text-xs text-muted-foreground">All healthy</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total GPUs</CardTitle>
            <HardDrive className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">52</div>
            <p className="text-xs text-muted-foreground">A100, T4, H100</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Pods</CardTitle>
            <Network className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">326</div>
            <p className="text-xs text-muted-foreground">Across all clusters</p>
          </CardContent>
        </Card>
      </div>

      <div className="space-y-4">
        {clusters.map((cluster) => (
          <Card key={cluster.name}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-blue-600">
                    <Server className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <CardTitle>{cluster.name}</CardTitle>
                    <CardDescription className="flex items-center gap-1">
                      <Globe className="h-3 w-3" />
                      {cluster.region}
                    </CardDescription>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <Badge variant={cluster.status === "healthy" ? "success" : "warning"}>
                    {cluster.status}
                  </Badge>
                  <Button variant="ghost" size="icon">
                    <Eye className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon">
                    <Settings className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-6">
                <div className="text-center p-3 rounded-lg bg-muted">
                  <p className="text-2xl font-bold">{cluster.nodes}</p>
                  <p className="text-xs text-muted-foreground">Nodes</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-muted">
                  <p className="text-2xl font-bold">{cluster.gpuCount}</p>
                  <p className="text-xs text-muted-foreground">GPUs</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-muted">
                  <p className="text-2xl font-bold">{cluster.cpuCores}</p>
                  <p className="text-xs text-muted-foreground">vCPUs</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-muted">
                  <p className="text-2xl font-bold">{cluster.memory}</p>
                  <p className="text-xs text-muted-foreground">Memory</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-muted">
                  <p className="text-2xl font-bold">{cluster.pods}</p>
                  <p className="text-xs text-muted-foreground">Pods</p>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Utilization</span>
                    <span className="font-medium">{cluster.utilization}%</span>
                  </div>
                  <Progress value={cluster.utilization} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
