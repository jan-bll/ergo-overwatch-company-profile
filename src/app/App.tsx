import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card";
import { Badge } from "@/app/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs";
import { 
  Building2, 
  AlertTriangle,
  MapPin,
  Factory,
  Users,
  Calendar,
  TrendingUp,
  Link2,
  Globe2,
  Package,
  Search,
  X,
  Clock,
  CheckCircle2,
  Loader2
} from "lucide-react";
import { 
  PieChart, 
  Pie, 
  Cell, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer
} from "recharts";
import React from "react";

export default function App() {
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [companyHistory, setCompanyHistory] = React.useState([
    {
      id: 1,
      name: "Dell Technologies Inc.",
      status: "completed",
      dateCompleted: "Jan 7, 2025",
      confidence: 78
    },
    {
      id: 2,
      name: "Procter & Gamble Co.",
      status: "in-progress",
      dateStarted: "Jan 14, 2025",
      progress: 45
    }
  ]);

  // Smooth scroll behavior
  React.useEffect(() => {
    document.documentElement.style.scrollBehavior = 'smooth';
    return () => {
      document.documentElement.style.scrollBehavior = 'auto';
    };
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const newCompany = {
        id: Date.now(),
        name: searchQuery.trim(),
        status: "in-progress",
        dateStarted: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        progress: 0
      };
      setCompanyHistory([newCompany, ...companyHistory]);
      setIsModalOpen(false);
      setSearchQuery("");
      
      // Simulate progress
      simulateProgress(newCompany.id);
    }
  };

  const simulateProgress = (companyId: number) => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 15;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        setCompanyHistory(prev => 
          prev.map(c => c.id === companyId 
            ? { ...c, status: "completed", dateCompleted: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }), confidence: Math.floor(Math.random() * 20) + 70 }
            : c
          )
        );
      }
      setCompanyHistory(prev => 
        prev.map(c => c.id === companyId ? { ...c, progress: Math.min(Math.floor(progress), 100) } : c)
      );
    }, 10000); // Update every 10 seconds
  };

  // Business Segments Data
  const businessSegmentsData = [
    { name: "Client Solutions Group", value: 55, color: "#1e3a8a" },
    { name: "Infrastructure Solutions Group", value: 40, color: "#3b82f6" },
    { name: "Other", value: 5, color: "#93c5fd" },
  ];

  // Geographic Revenue Data - Consistent Colors
  const REGION_COLORS = {
    Americas: "#1e3a8a",
    EMEA: "#3b82f6", 
    APJ: "#60a5fa"
  };

  const revenueDistributionData = [
    { name: "Americas", value: 50, color: REGION_COLORS.Americas },
    { name: "EMEA", value: 30, color: REGION_COLORS.EMEA },
    { name: "APJ", value: 20, color: REGION_COLORS.APJ },
  ];

  const yoyGrowthData = [
    { region: "Americas", growth: 5, fill: REGION_COLORS.Americas },
    { region: "EMEA", growth: -2, fill: REGION_COLORS.EMEA },
    { region: "APJ", growth: -8, fill: REGION_COLORS.APJ },
  ];

  const manufacturingData = [
    { country: "China", percentage: 40 },
    { country: "Malaysia", percentage: 25 },
    { country: "USA", percentage: 15 },
    { country: "Mexico", percentage: 10 },
    { country: "Brazil", percentage: 5 },
    { country: "Poland", percentage: 5 },
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Search Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full">
            <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-slate-900">New Company Research</h3>
              <button 
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-6">
              <form onSubmit={handleSearch}>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Company Name or Ticker
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="e.g., Apple Inc. or AAPL"
                    className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    autoFocus
                  />
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  Analysis will take approximately 10-15 minutes to complete
                </p>
                <div className="flex gap-3 mt-6">
                  <button
                    type="submit"
                    className="flex-1 px-4 py-2.5 bg-blue-700 hover:bg-blue-600 text-white text-sm font-medium rounded-lg transition-colors"
                  >
                    Start Research
                  </button>
                  <button
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-medium rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="bg-blue-950 border-b border-blue-900">
        <div className="max-w-[1600px] mx-auto px-8 py-6">
          <div className="flex items-end justify-between">
            <div>
              <h1 className="text-2xl font-light text-white tracking-tight">Company Profile — Deep Research</h1>
              <p className="text-sm text-blue-200 mt-1">Based on FY2024 10-K filed March 2024, supplemented with Q3 FY2025 earnings</p>
            </div>
            <div className="flex gap-3">
              <button 
                onClick={() => setIsModalOpen(true)}
                className="px-6 py-2.5 bg-emerald-700 hover:bg-emerald-600 text-white text-sm font-medium border border-emerald-600 hover:border-emerald-500 transition-colors shadow-sm"
              >
                New Research
              </button>
              <button 
                onClick={() => alert('Scenario analysis feature coming soon')}
                className="px-6 py-2.5 bg-blue-700 hover:bg-blue-600 text-white text-sm font-medium border border-blue-600 hover:border-blue-500 transition-colors shadow-sm"
              >
                Run Scenario Analysis
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Left Sidebar */}
        <aside className="w-64 bg-white border-r border-slate-200 sticky top-0 h-screen overflow-y-auto flex-shrink-0">
          <div className="p-6">
            {/* Logo/Brand */}
            <div className="mb-8 pb-6 border-b border-slate-200">
              <div className="text-xl font-light text-slate-900 tracking-tight">Ergo</div>
              <div className="text-xs text-slate-500 mt-0.5">Deep Research</div>
            </div>

            {/* Current Company Navigation */}
            <div className="mb-8">
              <div className="text-xs text-slate-500 uppercase tracking-wide mb-3">Current Report</div>
              <nav className="space-y-1">
                <a href="#overview" className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded transition-colors">
                  Overview
                </a>
                <a href="#segments" className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded transition-colors">
                  Business Segments
                </a>
                <a href="#geographic" className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded transition-colors">
                  Geographic
                </a>
                <a href="#supply-chain" className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded transition-colors">
                  Supply Chain
                </a>
                <a href="#flags" className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded transition-colors">
                  Flags
                </a>
              </nav>
            </div>

            {/* Company History */}
            <div className="pt-8 border-t border-slate-200">
              <div className="flex items-center justify-between mb-3">
                <div className="text-xs text-slate-500 uppercase tracking-wide">Research History</div>
                <button 
                  onClick={() => setIsModalOpen(true)}
                  className="text-blue-600 hover:text-blue-700 transition-colors"
                  title="New Research"
                >
                  <Search className="w-4 h-4" />
                </button>
              </div>
              <div className="space-y-3">
                {companyHistory.map((company) => (
                  <div 
                    key={company.id}
                    className={`p-3 border rounded-lg transition-all ${
                      company.status === 'completed' 
                        ? 'border-slate-200 bg-white hover:bg-slate-50 cursor-pointer' 
                        : 'border-blue-200 bg-blue-50'
                    }`}
                  >
                    <div className="flex items-start gap-2 mb-2">
                      {company.status === 'completed' ? (
                        <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                      ) : (
                        <Loader2 className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-slate-900 truncate">{company.name}</div>
                        <div className="text-xs text-slate-500 mt-0.5">
                          {company.status === 'completed' 
                            ? company.dateCompleted 
                            : `Started ${company.dateStarted}`
                          }
                        </div>
                      </div>
                    </div>
                    {company.status === 'in-progress' && (
                      <div className="space-y-1.5">
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-slate-600">Analyzing...</span>
                          <span className="text-slate-900 font-medium">{company.progress}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-blue-600 transition-all duration-500 ease-out"
                            style={{ width: `${company.progress}%` }}
                          />
                        </div>
                        <div className="text-xs text-slate-500 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          <span>~{Math.max(1, Math.ceil((100 - company.progress) / 10))} min remaining</span>
                        </div>
                      </div>
                    )}
                    {company.status === 'completed' && company.confidence && (
                      <div className="text-xs text-slate-600 mt-2">
                        Confidence: {company.confidence}%
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 max-w-[1400px] mx-auto px-8 py-8">
          {/* Company Header */}
          <div id="overview" className="bg-white border border-slate-200 mb-6">
            <div className="px-6 py-4 border-b border-slate-200 bg-slate-50">
              <h2 className="text-sm font-semibold text-slate-900 uppercase tracking-wide">Company Overview – Dell Technologies Inc.</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-4 gap-8 mb-6">
                <div>
                  <div className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Headquarters</div>
                  <div className="text-sm text-slate-900">Round Rock, USA</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Founded</div>
                  <div className="text-sm text-slate-900">1984</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Employees</div>
                  <div className="text-sm text-slate-900">120,000+</div>
                </div>
                <div>
                  <div className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Data Confidence</div>
                  <div className="text-sm text-slate-900">78%</div>
                </div>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed border-t border-slate-200 pt-4">
                Dell Technologies is a global technology company that designs, manufactures, and sells IT hardware, infrastructure, and related services. 
                Operations span client devices, enterprise infrastructure, and data center solutions, serving commercial, public sector, and consumer markets worldwide.
              </p>
            </div>
          </div>

          {/* Executive Snapshot */}
          <div className="bg-white border border-slate-200 mb-6">
            <div className="px-6 py-4 border-b border-slate-200 bg-slate-50">
              <h2 className="text-sm font-semibold text-slate-900 uppercase tracking-wide">Executive Snapshot</h2>
            </div>
            <div className="grid grid-cols-2 divide-x divide-slate-200">
              <div className="p-6 border-b border-slate-200">
                <div className="text-xs text-slate-500 mb-2 uppercase tracking-wide">Business Model</div>
                <div className="text-sm text-slate-900">Hybrid hardware, infrastructure, and services provider</div>
              </div>
              <div className="p-6 border-b border-slate-200">
                <div className="text-xs text-slate-500 mb-2 uppercase tracking-wide">Primary Revenue Driver</div>
                <div className="text-sm text-slate-900">Client Solutions and Infrastructure Solutions</div>
              </div>
              <div className="p-6">
                <div className="text-xs text-slate-500 mb-2 uppercase tracking-wide">Key Exposure</div>
                <div className="text-sm text-slate-900">Heavy dependence on advanced semiconductor supply chain in East Asia</div>
              </div>
              <div className="p-6">
                <div className="text-xs text-slate-500 mb-2 uppercase tracking-wide">Fiscal Year</div>
                <div className="text-sm text-slate-900">FY2024 | Midstream Value Chain Position</div>
              </div>
            </div>
          </div>

          {/* Main Grid */}
          <div className="grid grid-cols-12 gap-6 mb-6">
            {/* Business Segments */}
            <div id="segments" className="col-span-12">
              <div className="bg-white border border-slate-200 h-full">
                <div className="px-6 py-4 border-b border-slate-200 bg-slate-50">
                  <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wide">Business Segments</h3>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-3 gap-8">
                    <div className="col-span-1 flex items-center justify-center">
                      <div className="w-full max-w-[300px]">
                        <ResponsiveContainer width="100%" height={240}>
                          <PieChart>
                            <Pie
                              data={businessSegmentsData}
                              cx="50%"
                              cy="50%"
                              labelLine={false}
                              label={false}
                              outerRadius={80}
                              dataKey="value"
                              strokeWidth={2}
                              stroke="#ffffff"
                            >
                              {businessSegmentsData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                              ))}
                            </Pie>
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: 'white', 
                                border: '1px solid #e2e8f0',
                                fontSize: '12px',
                                borderRadius: '4px',
                                padding: '8px 12px'
                              }}
                            />
                          </PieChart>
                        </ResponsiveContainer>
                        <div className="mt-4 space-y-2">
                          {businessSegmentsData.map((entry, index) => (
                            <div key={index} className="flex items-center gap-2">
                              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }}></div>
                              <span className="text-xs text-slate-700">{entry.name}</span>
                              <span className="text-xs font-semibold text-slate-900 ml-auto">{entry.value}%</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                    <div className="col-span-2">
                      <div className="border border-slate-200">
                        <table className="w-full text-sm">
                          <thead className="bg-slate-50 border-b border-slate-200">
                            <tr>
                              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Segment</th>
                              <th className="px-4 py-3 text-right text-xs font-semibold text-slate-900 uppercase tracking-wide">% of Revenue</th>
                              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Key Products</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-200">
                            <tr className="hover:bg-slate-50">
                              <td className="px-4 py-3 text-slate-900">Client Solutions Group</td>
                              <td className="px-4 py-3 text-right text-slate-900">55%</td>
                              <td className="px-4 py-3 text-slate-700 text-xs">Desktops, notebooks, workstations</td>
                            </tr>
                            <tr className="hover:bg-slate-50">
                              <td className="px-4 py-3 text-slate-900">Infrastructure Solutions Group</td>
                              <td className="px-4 py-3 text-right text-slate-900">40%</td>
                              <td className="px-4 py-3 text-slate-700 text-xs">Servers, storage, networking</td>
                            </tr>
                            <tr className="hover:bg-slate-50">
                              <td className="px-4 py-3 text-slate-900">Other</td>
                              <td className="px-4 py-3 text-right text-slate-900">5%</td>
                              <td className="px-4 py-3 text-slate-700 text-xs">Services, financing, other</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div className="mt-4 text-xs text-slate-600 border-l-2 border-slate-300 pl-4">
                        Revenue is primarily driven by client devices and enterprise infrastructure. Client Solutions serves commercial, consumer, and education markets, while Infrastructure Solutions focuses on data center and enterprise IT.
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Geographic Exposure */}
          <div id="geographic" className="mb-6">
            <div className="bg-white border border-slate-200">
              <div className="px-6 py-4 border-b border-slate-200 bg-slate-50">
                <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wide">Geographic Exposure</h3>
              </div>
              <div className="p-6">
                <Tabs defaultValue="revenue" className="w-full">
                  <TabsList className="mb-6 bg-slate-100 border border-slate-200">
                    <TabsTrigger value="revenue" className="text-xs uppercase tracking-wide">Revenue</TabsTrigger>
                    <TabsTrigger value="manufacturing" className="text-xs uppercase tracking-wide">Manufacturing</TabsTrigger>
                    <TabsTrigger value="facilities" className="text-xs uppercase tracking-wide">Key Facilities</TabsTrigger>
                  </TabsList>

                  {/* Revenue Tab */}
                  <TabsContent value="revenue" className="space-y-6">
                    <div className="grid grid-cols-2 gap-8">
                      <div>
                        <h4 className="text-xs text-slate-500 mb-4 uppercase tracking-wide">Revenue Distribution</h4>
                        <div className="flex items-center justify-center">
                          <div className="w-full max-w-[340px]">
                            <ResponsiveContainer width="100%" height={220}>
                              <PieChart>
                                <Pie
                                  data={revenueDistributionData}
                                  cx="50%"
                                  cy="50%"
                                  labelLine={false}
                                  label={false}
                                  outerRadius={75}
                                  dataKey="value"
                                  strokeWidth={2}
                                  stroke="#ffffff"
                                >
                                  {revenueDistributionData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                  ))}
                                </Pie>
                                <Tooltip 
                                  contentStyle={{ 
                                    backgroundColor: 'white', 
                                    border: '1px solid #e2e8f0',
                                    fontSize: '12px',
                                    borderRadius: '4px',
                                    padding: '8px 12px'
                                  }}
                                />
                              </PieChart>
                            </ResponsiveContainer>
                            <div className="mt-4 space-y-2">
                              {revenueDistributionData.map((entry, index) => (
                                <div key={index} className="flex items-center gap-2">
                                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }}></div>
                                  <span className="text-xs text-slate-700">{entry.name}</span>
                                  <span className="text-xs font-semibold text-slate-900 ml-auto">{entry.value}%</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="text-xs text-slate-500 mb-4 uppercase tracking-wide">YoY Growth by Region</h4>
                        <ResponsiveContainer width="100%" height={220}>
                          <BarChart data={yoyGrowthData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                            <XAxis 
                              dataKey="region" 
                              tick={{ fill: '#64748b', fontSize: 10 }}
                              axisLine={{ stroke: '#cbd5e1' }}
                              tickLine={false}
                            />
                            <YAxis 
                              tick={{ fill: '#64748b', fontSize: 10 }}
                              axisLine={false}
                              tickLine={false}
                              domain={[-10, 10]}
                            />
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: 'white', 
                                border: '1px solid #e2e8f0',
                                fontSize: '12px',
                                borderRadius: '4px',
                                padding: '8px 12px'
                              }}
                            />
                            <Bar dataKey="growth" radius={0}>
                              {yoyGrowthData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.fill} />
                              ))}
                            </Bar>
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                    <div className="border-l-2 border-slate-300 pl-4 text-xs text-slate-600">
                      Revenue growth is concentrated in the Americas, while APJ shows year-over-year contraction.
                    </div>
                  </TabsContent>

                  {/* Manufacturing Tab */}
                  <TabsContent value="manufacturing" className="space-y-4">
                    <div>
                      <h4 className="text-xs text-slate-500 mb-4 uppercase tracking-wide">Manufacturing by Country (% of Production)</h4>
                      <ResponsiveContainer width="100%" height={240}>
                        <BarChart data={manufacturingData} layout="vertical">
                          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
                          <XAxis 
                            type="number" 
                            tick={{ fill: '#64748b', fontSize: 11 }}
                            axisLine={{ stroke: '#cbd5e1' }}
                            tickLine={false}
                          />
                          <YAxis 
                            dataKey="country" 
                            type="category" 
                            width={90}
                            tick={{ fill: '#64748b', fontSize: 11 }}
                            axisLine={false}
                            tickLine={false}
                          />
                          <Tooltip 
                            contentStyle={{ 
                              backgroundColor: 'white', 
                              border: '1px solid #e2e8f0',
                              fontSize: '12px'
                            }}
                          />
                          <Bar dataKey="percentage" fill="#1e3a8a" radius={0} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>

                    <div className="border border-slate-200">
                      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                        <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">Manufacturing Notes</h4>
                      </div>
                      <div className="divide-y divide-slate-200">
                        <div className="px-4 py-3">
                          <div className="flex items-start gap-3">
                            <div className="text-xs font-semibold text-slate-900 w-20 flex-shrink-0">China</div>
                            <div className="text-xs text-slate-700">Primary manufacturing hub through contract manufacturers; Xiamen and Chengdu facilities</div>
                          </div>
                        </div>
                        <div className="px-4 py-3">
                          <div className="flex items-start gap-3">
                            <div className="text-xs font-semibold text-slate-900 w-20 flex-shrink-0">Malaysia</div>
                            <div className="text-xs text-slate-700">Penang facility - key alternative to China operations</div>
                          </div>
                        </div>
                        <div className="px-4 py-3">
                          <div className="flex items-start gap-3">
                            <div className="text-xs font-semibold text-slate-900 w-20 flex-shrink-0">USA</div>
                            <div className="text-xs text-slate-700">Austin, TX - primarily enterprise and custom configurations</div>
                          </div>
                        </div>
                        <div className="px-4 py-3">
                          <div className="flex items-start gap-3">
                            <div className="text-xs font-semibold text-slate-900 w-20 flex-shrink-0">Mexico</div>
                            <div className="text-xs text-slate-700">Expanding capacity for USMCA benefits</div>
                          </div>
                        </div>
                        <div className="px-4 py-3">
                          <div className="flex items-start gap-3">
                            <div className="text-xs font-semibold text-slate-900 w-20 flex-shrink-0">Brazil</div>
                            <div className="text-xs text-slate-700">Regional assembly for Latin America</div>
                          </div>
                        </div>
                        <div className="px-4 py-3">
                          <div className="flex items-start gap-3">
                            <div className="text-xs font-semibold text-slate-900 w-20 flex-shrink-0">Poland</div>
                            <div className="text-xs text-slate-700">European regional hub</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="border-l-2 border-amber-600 pl-4 text-xs text-slate-700 bg-amber-50 -ml-6 pl-6 py-3">
                      Manufacturing is heavily concentrated in China, creating geopolitical and trade risk exposure.
                    </div>
                  </TabsContent>

                  {/* Key Facilities Tab */}
                  <TabsContent value="facilities" className="space-y-3">
                    <div className="border border-slate-200">
                      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                        <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">Round Rock Campus — USA</h4>
                      </div>
                      <div className="p-4">
                        <div className="grid grid-cols-4 gap-4 text-xs">
                          <div>
                            <div className="text-slate-500 mb-1">Type</div>
                            <div className="text-slate-900">Headquarters</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Function</div>
                            <div className="text-slate-900">Global headquarters, executive offices, R&D</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Significance</div>
                            <div className="text-slate-900">Command center for global operations, houses key decision-making</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Source</div>
                            <div className="text-slate-900">Tier 1 - SEC Filing</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="border border-slate-200">
                      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                        <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">Xiamen Manufacturing — China</h4>
                      </div>
                      <div className="p-4">
                        <div className="grid grid-cols-4 gap-4 text-xs">
                          <div>
                            <div className="text-slate-500 mb-1">Type</div>
                            <div className="text-slate-900">Manufacturing</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Function</div>
                            <div className="text-slate-900">PC and server assembly</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Significance</div>
                            <div className="text-slate-900">Largest manufacturing facility, ~25% of total production</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Source</div>
                            <div className="text-slate-900">Tier 2 - Official</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="border border-slate-200">
                      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                        <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">Penang Operations — Malaysia</h4>
                      </div>
                      <div className="p-4">
                        <div className="grid grid-cols-4 gap-4 text-xs">
                          <div>
                            <div className="text-slate-500 mb-1">Type</div>
                            <div className="text-slate-900">Manufacturing</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Function</div>
                            <div className="text-slate-900">Server and storage manufacturing</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Significance</div>
                            <div className="text-slate-900">Primary non-China manufacturing hub, strategic diversification</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Source</div>
                            <div className="text-slate-900">Tier 2 - Official</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="border border-slate-200">
                      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                        <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">Austin Manufacturing — USA</h4>
                      </div>
                      <div className="p-4">
                        <div className="grid grid-cols-4 gap-4 text-xs">
                          <div>
                            <div className="text-slate-500 mb-1">Type</div>
                            <div className="text-slate-900">Manufacturing</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Function</div>
                            <div className="text-slate-900">Enterprise servers, custom configurations</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Significance</div>
                            <div className="text-slate-900">Made-in-USA capability for federal and security-sensitive customers</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Source</div>
                            <div className="text-slate-900">Tier 2 - Official</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="border border-slate-200">
                      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                        <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">Limerick Campus — Ireland</h4>
                      </div>
                      <div className="p-4">
                        <div className="grid grid-cols-4 gap-4 text-xs">
                          <div>
                            <div className="text-slate-500 mb-1">Type</div>
                            <div className="text-slate-900">R&D</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Function</div>
                            <div className="text-slate-900">EMEA headquarters, software development, customer support</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Significance</div>
                            <div className="text-slate-900">European hub for operations and R&D</div>
                          </div>
                          <div>
                            <div className="text-slate-500 mb-1">Source</div>
                            <div className="text-slate-900">Tier 2 - Official</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </div>
            </div>
          </div>

          {/* Supply Chain Dependencies */}
          <div id="supply-chain" className="bg-white border border-slate-200 mb-6">
            <div className="px-6 py-4 border-b border-slate-200 bg-slate-50">
              <h2 className="text-sm font-semibold text-slate-900 uppercase tracking-wide">Supply Chain Dependencies</h2>
            </div>
            <div className="p-6">
              <Tabs defaultValue="suppliers" className="w-full">
                <TabsList className="mb-6 bg-slate-100 border border-slate-200">
                  <TabsTrigger value="suppliers" className="text-xs uppercase tracking-wide">Critical Suppliers</TabsTrigger>
                  <TabsTrigger value="manufacturers" className="text-xs uppercase tracking-wide">Contract Manufacturers</TabsTrigger>
                  <TabsTrigger value="concentration" className="text-xs uppercase tracking-wide">Geographic Concentration</TabsTrigger>
                </TabsList>

                {/* Critical Suppliers Tab */}
                <TabsContent value="suppliers">
                  <div className="border border-slate-200">
                    <table className="w-full text-sm">
                      <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Supplier</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Provides</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Risk</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Classification</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-200">
                        <tr className="bg-red-50">
                          <td colSpan={4} className="px-4 py-2 text-xs font-semibold text-red-900 uppercase tracking-wide">
                            🔴 Critical Dependencies
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Intel Corporation (USA)</td>
                          <td className="px-4 py-3 text-slate-700">CPUs for PCs and servers (x86 processors)</td>
                          <td className="px-4 py-3 text-slate-700">Primary CPU supplier; AMD is alternative but Intel dominates enterprise</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-red-100 text-red-800 border border-red-200">CRITICAL</span>
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">NVIDIA Corporation (USA)</td>
                          <td className="px-4 py-3 text-slate-700">GPUs for AI servers, workstations, gaming</td>
                          <td className="px-4 py-3 text-slate-700">Near-monopoly on AI/ML accelerators; H100/B200 GPUs critical for AI server demand</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-red-100 text-red-800 border border-red-200">SINGLE SOURCE</span>
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">TSMC (Taiwan Semiconductor) (Taiwan)</td>
                          <td className="px-4 py-3 text-slate-700">Semiconductor fabrication (indirect - via Intel, NVIDIA, AMD)</td>
                          <td className="px-4 py-3 text-slate-700">Not direct supplier but manufactures chips for key suppliers; single point of failure for advanced nodes</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-red-100 text-red-800 border border-red-200">SINGLE SOURCE</span>
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Microsoft Corporation (USA)</td>
                          <td className="px-4 py-3 text-slate-700">Windows OS licenses, software ecosystem</td>
                          <td className="px-4 py-3 text-slate-700">Windows pre-installed on virtually all Dell PCs; no viable alternative for enterprise</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-red-100 text-red-800 border border-red-200">SINGLE SOURCE</span>
                          </td>
                        </tr>
                        <tr className="bg-orange-50">
                          <td colSpan={4} className="px-4 py-2 text-xs font-semibold text-orange-900 uppercase tracking-wide">
                            🟠 High Dependencies
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">AMD (Advanced Micro Devices) (USA)</td>
                          <td className="px-4 py-3 text-slate-700">CPUs and GPUs for PCs and servers</td>
                          <td className="px-4 py-3 text-slate-700">Growing share in server CPUs (EPYC), secondary PC CPU supplier</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-orange-100 text-orange-800 border border-orange-200">HIGH</span>
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Samsung Electronics (South Korea)</td>
                          <td className="px-4 py-3 text-slate-700">DRAM, NAND flash memory, SSDs</td>
                          <td className="px-4 py-3 text-slate-700">One of three major memory suppliers (with SK Hynix, Micron)</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-orange-100 text-orange-800 border border-orange-200">HIGH</span>
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">SK Hynix (South Korea)</td>
                          <td className="px-4 py-3 text-slate-700">DRAM, NAND flash, HBM for AI</td>
                          <td className="px-4 py-3 text-slate-700">Critical for HBM (High Bandwidth Memory) for AI servers</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-orange-100 text-orange-800 border border-orange-200">HIGH</span>
                          </td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Micron Technology (USA)</td>
                          <td className="px-4 py-3 text-slate-700">DRAM, NAND flash memory</td>
                          <td className="px-4 py-3 text-slate-700">US-based memory supplier; diversification from Korean suppliers</td>
                          <td className="px-4 py-3">
                            <span className="inline-block px-2 py-1 text-xs bg-orange-100 text-orange-800 border border-orange-200">HIGH</span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </TabsContent>

                {/* Contract Manufacturers Tab */}
                <TabsContent value="manufacturers">
                  <div className="border border-slate-200">
                    <table className="w-full text-sm">
                      <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Manufacturer</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Production Locations</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-slate-900 uppercase tracking-wide">Products</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-200">
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Foxconn (Hon Hai) (Taiwan)</td>
                          <td className="px-4 py-3 text-slate-700">China, Vietnam, India, Mexico</td>
                          <td className="px-4 py-3 text-slate-700">Consumer PCs, monitors, some servers</td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Wistron (Taiwan)</td>
                          <td className="px-4 py-3 text-slate-700">China, Taiwan, India</td>
                          <td className="px-4 py-3 text-slate-700">Notebooks, desktop PCs</td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Compal Electronics (Taiwan)</td>
                          <td className="px-4 py-3 text-slate-700">China, Vietnam</td>
                          <td className="px-4 py-3 text-slate-700">Notebooks, monitors</td>
                        </tr>
                        <tr className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-900">Quanta Computer (Taiwan)</td>
                          <td className="px-4 py-3 text-slate-700">China, Taiwan</td>
                          <td className="px-4 py-3 text-slate-700">Servers, cloud infrastructure</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </TabsContent>

                {/* Geographic Concentration Tab */}
                <TabsContent value="concentration" className="space-y-4">
                  <div className="border border-slate-200">
                    <div className="px-4 py-3 bg-slate-50 border-b border-slate-200">
                      <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wide">Summary</h4>
                    </div>
                    <div className="p-4">
                      <div className="grid grid-cols-3 gap-6 text-sm mb-6">
                        <div>
                          <div className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Top Country</div>
                          <div className="text-lg font-light text-slate-900">Taiwan</div>
                        </div>
                        <div>
                          <div className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Concentration</div>
                          <div className="text-lg font-light text-slate-900">45%</div>
                        </div>
                        <div>
                          <div className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Top 3 Countries</div>
                          <div className="text-sm text-slate-900">Taiwan</div>
                          <div className="text-sm text-slate-900">China</div>
                          <div className="text-sm text-slate-900">South Korea</div>
                        </div>
                      </div>
                      <div className="border-l-2 border-slate-300 pl-4 text-xs text-slate-600">
                        Heavy reliance on Taiwan (TSMC, ODMs) and China (manufacturing). Korean memory suppliers diversify somewhat but still concentrated in East Asia.
                      </div>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          </div>

          {/* Concentration & Risk Flags */}
          <div id="flags" className="bg-white border border-slate-200 shadow-sm">
            <div className="px-6 py-4 border-b border-slate-200 bg-slate-50">
              <h2 className="text-sm font-semibold text-slate-900 uppercase tracking-wide">Concentration & Risk Flags</h2>
            </div>
            <div className="divide-y divide-slate-200">
              <div className="p-6 flex items-start gap-6">
                <div className="w-1.5 h-20 bg-red-600 rounded-full flex-shrink-0"></div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-block px-2 py-0.5 text-xs font-semibold bg-red-100 text-red-800 border border-red-200 rounded">MANUFACTURING</span>
                    <span className="text-xs text-slate-500">Critical Risk</span>
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">40% of manufacturing concentrated in China</h3>
                  <p className="text-sm text-slate-600 leading-relaxed">Primary manufacturing through contract manufacturers in Xiamen and Chengdu regions; vulnerable to US-China trade tensions and potential supply disruption</p>
                </div>
              </div>

              <div className="p-6 flex items-start gap-6">
                <div className="w-1.5 h-20 bg-orange-600 rounded-full flex-shrink-0"></div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-block px-2 py-0.5 text-xs font-semibold bg-orange-100 text-orange-800 border border-orange-200 rounded">SUPPLIER</span>
                    <span className="text-xs text-slate-500">High Risk</span>
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Critical dependency on Taiwan semiconductor ecosystem</h3>
                  <p className="text-sm text-slate-600 leading-relaxed">TSMC fabricates chips for key suppliers (Intel, NVIDIA, AMD); Taiwan contract manufacturers (Foxconn, Wistron, Compal) handle significant production volume</p>
                </div>
              </div>

              <div className="p-6 flex items-start gap-6">
                <div className="w-1.5 h-20 bg-amber-600 rounded-full flex-shrink-0"></div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-block px-2 py-0.5 text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200 rounded">SUPPLIER</span>
                    <span className="text-xs text-slate-500">High Risk</span>
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">NVIDIA near-monopoly on AI accelerators</h3>
                  <p className="text-sm text-slate-600 leading-relaxed">AI server demand dependent on NVIDIA GPU supply; limited alternatives for high-performance AI training</p>
                </div>
              </div>

              <div className="p-6 flex items-start gap-6">
                <div className="w-1.5 h-20 bg-yellow-600 rounded-full flex-shrink-0"></div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-block px-2 py-0.5 text-xs font-semibold bg-yellow-100 text-yellow-800 border border-yellow-200 rounded">SUPPLIER</span>
                    <span className="text-xs text-slate-500">Medium Risk</span>
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Memory supplier concentration in East Asia</h3>
                  <p className="text-sm text-slate-600 leading-relaxed">Samsung, SK Hynix (Korea) and Micron (US, but Asian fabs) dominate memory supply; HBM for AI particularly concentrated</p>
                </div>
              </div>

              <div className="p-6 flex items-start gap-6">
                <div className="w-1.5 h-20 bg-blue-600 rounded-full flex-shrink-0"></div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-block px-2 py-0.5 text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200 rounded">REGULATORY</span>
                    <span className="text-xs text-slate-500">Regulatory Risk</span>
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Export control exposure on AI products to China</h3>
                  <p className="text-sm text-slate-600 leading-relaxed">BIS restrictions on advanced AI chip exports to China limit high-margin server sales to second-largest market</p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}