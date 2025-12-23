import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface InputFormProps {
  inputText: string
  setInputText: (text: string) => void
  setPreviewData: (data: any) => void
  isGenerating: boolean
}

export default function InputForm({ 
  inputText, 
  setInputText, 
  setPreviewData,
  isGenerating 
}: InputFormProps) {
  const [loading, setLoading] = useState(false)

  const handlePreview = async () => {
    if (!inputText.trim()) return

    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/preview`, {
        input_text: inputText,
        include_speaker_notes: true
      })
      setPreviewData(response.data)
    } catch (error) {
      console.error('Preview error:', error)
      alert('Failed to generate preview. Please check your input and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Enter your content
        </label>
        <textarea
          className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent resize-none"
          placeholder="Enter a topic, bullet points, or full outline...&#10;&#10;Examples:&#10;• Explain Machine Learning&#10;• Introduction&#10;  - What is ML?&#10;  - Why it matters&#10;• Key Concepts&#10;  - Supervised Learning&#10;  - Unsupervised Learning"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          disabled={isGenerating}
        />
      </div>

      <button
        onClick={handlePreview}
        disabled={loading || isGenerating || !inputText.trim()}
        className="w-full bg-secondary text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
      >
        {loading ? 'Generating Preview...' : 'Preview Slides'}
      </button>

      <div className="text-sm text-gray-600">
        <p className="font-medium mb-2">Tip: You can input:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>A simple topic (e.g., "Explain Large Language Models")</li>
          <li>A list of bullet points (one per slide)</li>
          <li>A full outline with nested bullets</li>
        </ul>
      </div>
    </div>
  )
}
