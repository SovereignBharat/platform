"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Shield, Key, Users, Lock, Eye, FileText, AlertTriangle,
  CheckCircle, Clock, ShieldCheck, KeyRound
} from "lucide-react"

const apiKeys = [
  { name: "Production API Key", key: "sb_prod_•••••••••••3f8a", created: "2024-01-15", lastUsed: "2 min ago" },
  { name: "Development Key", key: "sb_dev_•••••••••••9b2c", created: "2024-01-18", lastUsed: "1 hour ago" },
  { name: "CI/CD Pipeline", key: "sb_cicd_•••••••••••7d4e", created: "2024-01-20", lastUsed: "3 hours ago" },
]

const policies = [
  { name: "RBAC Default", description: "Role-based access control for platform users", status: "active" },
  { name: "Data Residency", description: "All data must remain within India region", status: "active" },
  { name: "GPU Allocation", description: "GPU resources limited by tenant quota", status: "active" },
]

const auditLogs = [
  { action: "User login", user: "admin@sovereignbharat.in", time: "2024-01-26 10:30:45" },
  { action: "API key created", user: "dev@startup.io", time: "2024-01-26 10:25:12" },
  { action: "Model deployed", user: "admin@sovereignbharat.in", time: "2024-01-26 10:15:33" },
  { action: "Policy modified", user: "security-team", time: "2024-01-26 09:45:18" },
  { action: "Cluster scaled", user: "system", time: "2024-01-26 09:30:00" },
]

export default function SecurityPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Security & Governance</h1>
          <p className="text-muted-foreground">Manage access control, policies, and audit compliance</p>
        </div>
        <Button>
          <Shield className="mr-2 h-4 w-4" />
          Security Scan
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Security Score</CardTitle>
            <ShieldCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">98/100</div>
            <p className="text-xs text-muted-foreground">All checks passed</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Active Policies</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">All enforced</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">API Keys</CardTitle>
            <Key className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">3 active today</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Data Residency</CardTitle>
            <Lock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Badge variant="success">India Only</Badge>
            </div>
            <p className="text-xs text-muted-foreground">Compliant</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="access">
        <TabsList>
          <TabsTrigger value="access">Access Control</TabsTrigger>
          <TabsTrigger value="policies">Policies</TabsTrigger>
          <TabsTrigger value="audit">Audit Logs</TabsTrigger>
          <TabsTrigger value="keys">API Keys</TabsTrigger>
        </TabsList>

        <TabsContent value="access" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Role-Based Access
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                        <Shield className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium">Admin</p>
                        <p className="text-sm text-muted-foreground">Full platform access</p>
                      </div>
                    </div>
                    <Badge>5 users</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-100">
                        <KeyRound className="h-5 w-5 text-green-600" />
                      </div>
                      <div>
                        <p className="font-medium">Developer</p>
                        <p className="text-sm text-muted-foreground">Deploy and manage resources</p>
                      </div>
                    </div>
                    <Badge>24 users</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100">
                        <Eye className="h-5 w-5 text-purple-600" />
                      </div>
                      <div>
                        <p className="font-medium">Viewer</p>
                        <p className="text-sm text-muted-foreground">Read-only access</p>
                      </div>
                    </div>
                    <Badge>8 users</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Authentication Methods
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span>OAuth 2.0 / OIDC</span>
                    </div>
                    <Badge variant="success">Enabled</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span>JWT Tokens</span>
                    </div>
                    <Badge variant="success">Enabled</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span>API Key Auth</span>
                    </div>
                    <Badge variant="success">Enabled</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <Clock className="h-5 w-5 text-amber-600" />
                      <span>MFA / 2FA</span>
                    </div>
                    <Badge variant="warning">Optional</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="policies" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Active Policies</CardTitle>
                  <CardDescription>Platform governance and security policies</CardDescription>
                </div>
                <Button variant="outline">
                  <FileText className="mr-2 h-4 w-4" />
                  Create Policy
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {policies.map((policy) => (
                  <div key={policy.name} className="flex items-center justify-between p-4 rounded-lg border">
                    <div>
                      <p className="font-medium">{policy.name}</p>
                      <p className="text-sm text-muted-foreground">{policy.description}</p>
                    </div>
                    <Badge variant="success">{policy.status}</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="audit" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Audit Logs</CardTitle>
              <CardDescription>Complete history of platform activities</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="grid grid-cols-3 gap-4 border-b pb-3 text-sm font-medium text-muted-foreground">
                  <div>Action</div>
                  <div>User</div>
                  <div>Timestamp</div>
                </div>
                {auditLogs.map((log, index) => (
                  <div key={index} className="grid grid-cols-3 gap-4 py-3 border-b last:border-0">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                      {log.action}
                    </div>
                    <div className="text-sm">{log.user}</div>
                    <div className="text-sm text-muted-foreground">{log.time}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="keys" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>API Keys</CardTitle>
                  <CardDescription>Manage your API access credentials</CardDescription>
                </div>
                <Button>
                  <Key className="mr-2 h-4 w-4" />
                  Create Key
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {apiKeys.map((apiKey) => (
                  <div key={apiKey.name} className="flex items-center justify-between p-4 rounded-lg border">
                    <div>
                      <p className="font-medium">{apiKey.name}</p>
                      <code className="text-sm text-muted-foreground">{apiKey.key}</code>
                      <p className="text-xs text-muted-foreground mt-1">
                        Created: {apiKey.created} • Last used: {apiKey.lastUsed}
                      </p>
                    </div>
                    <Button variant="destructive" size="sm">Revoke</Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
