"use client";

import { useState, useEffect } from "react";
import {
  Plus,
  FileText,
  Search,
  Filter,
  ExternalLink,
  Download,
  Clock,
  FileCode,
  CheckCircle2,
  BookOpen,
  Rocket,
  ShieldCheck,
  Upload
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import { DocumentType } from "@prisma/client";

// Mapping enum to readable labels and icons
const categoryInfo: Record<DocumentType, { label: string; icon: any; color: string }> = {
  BUSINESS_PROBLEM: { label: "Business Problem", icon: FileText, color: "text-red-400" },
  BUSINESS_SOLUTION_CONCEPT: { label: "Solution Concept", icon: BookOpen, color: "text-blue-400" },
  BUSINESS_SOLUTION_SPEC: { label: "Product Spec", icon: CheckCircle2, color: "text-green-400" },
  TECHNICAL_DESIGN_FRONTEND: { label: "Frontend Design", icon: FileCode, color: "text-orange-400" },
  TECHNICAL_DESIGN_BACKEND: { label: "Backend Design", icon: FileCode, color: "text-purple-400" },
  TEST_VERIFICATION: { label: "Verification Guide", icon: ShieldCheck, color: "text-cyan-400" },
  QA_BENCHMARKS: { label: "QA Benchmarks", icon: ShieldCheck, color: "text-pink-400" },
  USER_MANUAL: { label: "User Manual", icon: BookOpen, color: "text-yellow-400" },
  RELEASE_DOCUMENT: { label: "Release Doc", icon: Rocket, color: "text-indigo-400" },
};

export default function Dashboard() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedType, setSelectedType] = useState<DocumentType | "ALL">("ALL");
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, [selectedType]);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const url = selectedType === "ALL" ? "/api/documents" : `/api/documents?type=${selectedType}`;
      const res = await axios.get(url);
      setDocuments(res.data);
    } catch (error) {
      console.error("Fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredDocs = documents.filter(doc =>
    doc.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
        <div>
          <h1 className="text-4xl font-bold font-outfit gradient-text mb-2">DevDoc Manager</h1>
          <p className="text-gray-400">Streamline your development documentation lifecycle.</p>
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-xl font-medium transition-all shadow-lg shadow-blue-600/20"
        >
          <Plus size={20} />
          Add Document
        </motion.button>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input
            type="text"
            placeholder="Search documents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-3 glass bg-transparent focus:outline-none focus:border-blue-500/50 transition-all"
          />
        </div>
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
          <button
            onClick={() => setSelectedType("ALL")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${selectedType === "ALL" ? "bg-white/10 text-white border border-white/20" : "text-gray-400 hover:text-white"
              }`}
          >
            All Docs
          </button>
          {Object.entries(categoryInfo).map(([type, info]) => (
            <button
              key={type}
              onClick={() => setSelectedType(type as DocumentType)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${selectedType === type ? "bg-white/10 text-white border border-white/20" : "text-gray-400 hover:text-white"
                }`}
            >
              {info.label}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-48 glass animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <AnimatePresence mode="popLayout">
            {filteredDocs.map((doc) => {
              const info = categoryInfo[doc.type as DocumentType];
              const Icon = info.icon;
              return (
                <motion.div
                  key={doc.id}
                  layout
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="glass p-6 glass-hover group"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`p-3 rounded-xl bg-white/5 ${info.color}`}>
                      <Icon size={24} />
                    </div>
                    <div className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock size={12} />
                      {new Date(doc.createdAt).toLocaleDateString()}
                    </div>
                  </div>
                  <h3 className="text-lg font-semibold mb-2 line-clamp-1">{doc.title}</h3>
                  <p className="text-gray-400 text-sm mb-6 line-clamp-2">
                    {doc.content || "Uploaded document or external link."}
                  </p>
                  <div className="flex items-center gap-3 mt-auto">
                    {doc.fileUrl && (
                      <a
                        href={doc.fileUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-sm transition-all"
                      >
                        <Download size={14} /> View File
                      </a>
                    )}
                    {doc.externalLink && (
                      <a
                        href={doc.externalLink}
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-sm transition-all"
                      >
                        <ExternalLink size={14} /> Reference
                      </a>
                    )}
                    {!doc.fileUrl && !doc.externalLink && (
                      <button className="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-sm transition-all">
                        <FileText size={14} /> Read Manual
                      </button>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      )}

      {/* Empty State */}
      {!loading && filteredDocs.length === 0 && (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mb-6 text-gray-500">
            <Filter size={32} />
          </div>
          <h3 className="text-xl font-medium text-gray-300">No documents found</h3>
          <p className="text-gray-500 max-w-xs mx-auto mt-2">
            Try adjusting your search or category filters, or add a new document to get started.
          </p>
        </div>
      )}

      {/* Modal Placeholder */}
      <AnimatePresence>
        {isModalOpen && (
          <DocumentModal
            onClose={() => setIsModalOpen(false)}
            onSuccess={() => {
              setIsModalOpen(false);
              fetchDocuments();
            }}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

// Sub-component for the Modal (Implementing in the same file for brevity but good practice to split)
function DocumentModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [formData, setFormData] = useState({
    title: "",
    type: "BUSINESS_PROBLEM" as DocumentType,
    content: "",
    externalLink: "",
  });
  const [file, setFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      let fileUrl = "";

      let uploadedFileKey = "";
      if (file) {
        // 1. Single server-side upload call
        const formDataUpload = new FormData();
        formDataUpload.append("file", file);

        const { data: { url, key } } = await axios.post("/api/upload", formDataUpload, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        // 2. Set the file URL and key returned by the server
        fileUrl = url;
        uploadedFileKey = key;
      }

      await axios.post("/api/documents", {
        ...formData,
        fileUrl,
        fileKey: uploadedFileKey,
      });

      onSuccess();
    } catch (error) {
      console.error("Submit error:", error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.9, opacity: 0, y: 20 }}
        className="glass w-full max-w-lg p-8 overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-2xl font-bold font-outfit mb-6">New Document</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Title</label>
            <input
              required
              value={formData.title}
              onChange={e => setFormData({ ...formData, title: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Type</label>
              <select
                value={formData.type}
                onChange={e => setFormData({ ...formData, type: e.target.value as DocumentType })}
                className="w-full bg-[#1a1a1a] border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
              >
                {Object.entries(categoryInfo).map(([type, info]) => (
                  <option key={type} value={type}>{info.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">External Link (Optional)</label>
              <input
                type="url"
                value={formData.externalLink}
                onChange={e => setFormData({ ...formData, externalLink: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Manual Content / Notes</label>
            <textarea
              rows={4}
              value={formData.content}
              onChange={e => setFormData({ ...formData, content: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
            />
          </div>
          <div className="border-2 border-dashed border-white/10 rounded-xl p-6 text-center hover:border-blue-500/50 transition-all cursor-pointer relative">
            <input
              type="file"
              className="absolute inset-0 opacity-0 cursor-pointer"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            <div className="flex flex-col items-center">
              <Upload className="text-gray-500 mb-2" />
              <p className="text-sm text-gray-300">
                {file ? file.name : "Click to upload file or drag & drop"}
              </p>
              <p className="text-xs text-gray-500 mt-1">PDF, DOCX, Images supported</p>
            </div>
          </div>
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 transition-all"
            >
              Cancel
            </button>
            <button
              disabled={submitting}
              type="submit"
              className="flex-1 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-50 transition-all"
            >
              {submitting ? "Processing..." : "Create Document"}
            </button>
          </div>
        </form>
      </motion.div>
    </motion.div>
  );
}
