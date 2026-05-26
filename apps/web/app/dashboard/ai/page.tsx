"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import {
  Cpu, HardDrive, Network, Plus, Play, Pause, Settings, 
  ChevronRight, MemoryStick, Gauge, Zap, Brain
} from "lucide-react"

const models = [
  { id: 1, name: "BharatLLM-13B", type: "LLM", status: "deployed", replicas: 4, gpu: "A100", memory: "26GB", latency: "45ms" },
  { id: 2, name: "BharatLLM-7B", type: "LLM", status: "deployed", replicas: 3, gpu: "A100", memory: "14GB", latency: "32ms" },
  { id: 3, name: "IndicBERT-3B", type: "Embedding", status: "deployed", replicas: 2, gpu: "T4", memory: "6GB", latency: "12ms" },
  { id: 4, name: "SentinelAI-1B", type: "Security", status: "scaling", replicas: 2, gpu: "A100", memory: "2GB", latency: "28ms" },
]

const gpuPools = [
  { name: "NVIDIA A100 Pool", available: 12, total: 24, utilization: 50 },
  { name: "NVIDIA T4 Pool", available: 8, total: 16, utilization: 50 },
  { name: "NVIDIA H100 Pool", available: 4, total: 8, utilization: 50 },
]

const endpoints = [
  { name: "Chat Completions", path: "/v1/chat/completions", method: "POST", status: "active" },
  { name: "Embeddings", path: "/v1/embeddings", method: "POST", status: "active" },
  { name: "Model List", path: "/v1/models", method: "GET", status: "active" },
]

export default function AIPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">AI Infrastructure</h1>
          <p className="text-muted-foreground">Manage models, inference endpoints, and GPU resources</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Deploy Model
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Deployed Models</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">4 LLM, 8 embedding</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">GPU Utilization</CardTitle>
            <Cpu className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">67%</div>
            <Progress value={67} className="mt-2" />
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Avg Latency</CardTitle>
            <Gauge className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">28ms</div>
            <p className="text-xs text-muted-foreground">p50 across all models</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Requests</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2.4M</div>
            <p className="text-xs text-muted-foreground">Last 24 hours</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="models">
        <TabsList>
          <TabsTrigger value="models">Models</TabsTrigger>
          <TabsTrigger value="gpu">GPU Pools</TabsTrigger>
          <TabsTrigger value="endpoints">Endpoints</TabsTrigger>
          <TabsTrigger value="deploy">Quick Deploy</TabsTrigger>
        </TabsList>

        <TabsContent value="models" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Model Registry</CardTitle>
                  <CardDescription>Manage deployed AI models and their configurations</CardDescription>
                </div>
                <Input placeholder="Search models..." className="w-64" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {models.map((model) => (
                  <div key={model.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-accent/50 transition-colors">
                    <div className="flex items-center gap-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-purple-500 to-blue-600">
                        <Brain className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="font-semibold">{model.name}</p>
                          <Badge variant="secondary">{model.type}</Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                          <span className="flex items-center gap-1">
                            <MemoryStick className="h-3 w-3" />
                            {model.memory}
                          </span>
                          <span className="flex items-center gap-1">
                            <Cpu className="h-3 w-3" />
                            {model.gpu}
                          </span>
                          <span className="flex items-center gap-1">
                            <Gauge className="h-3 w-3" />
                            {model.latency}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right mr-4">
                        <p className="text-sm font-medium">{model.replicas} replicas</p>
                        <p className="text-xs text-muted-foreground">Auto-scaling</p>
                      </div>
                      <Button variant="ghost" size="icon">
                        <Settings className="h-4 w-4" />
                      </Button>
                      <Badge variant={model.status === "deployed" ? "success" : "warning"}>
                        {model.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="gpu" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {gpuPools.map((pool) => (
              <Card key={pool.name}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm">{pool.name}</CardTitle>
                    <Badge variant="success">Active</Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-muted-foreground text-sm">Available</p>
                      <p className="text-2xl font-bold">{pool.available}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground text-sm">Total</p>
                      <p className="text-2xl font-bold">{pool.total}</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Utilization</span>
                      <span className="font-medium">{pool.utilization}%</span>
                    </div>
                    <Progress value={pool.utilization} />
                  </div>
                  <Button variant="outline" className="w-full">
                    Manage Pool
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="endpoints" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Endpoints</CardTitle>
              <CardDescription>OpenAI-compatible inference endpoints</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {endpoints.map((endpoint, index) => (
                  <div key={index} className="flex items-center justify-between p-4 rounded-lg border">
                    <div>
                      <p className="font-medium">{endpoint.name}</p>
                      <code className="text-sm text-muted-foreground">{endpoint.path}</code>
                    </div>
                    <div className="flex items-center gap-4">
                      <Badge variant="outline">{endpoint.method}</Badge>
                      <Badge variant="success">{endpoint.status}</Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="deploy" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Quick Deploy</CardTitle>
              <CardDescription>Deploy a new model in minutes</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Model Name</label>
                  <Input placeholder="e.g., bharat-llm-7b" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Model Type</label>
                  <Input placeholder="e.g., text-generation" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">GPU Type</label>
                  <Input placeholder="e.g., A100" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Replicas</label>
                  <Input type="number" placeholder="2" defaultValue="2" />
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="outline">Cancel</Button>
                <Button>
                  <Play className="mr-2 h-4 w-4" />
                  Deploy Model
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
