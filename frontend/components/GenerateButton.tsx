import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface GenerateButtonProps {
  inputText: string
  isGenerating: boolean
  setIsGenerating: (generating: boolean) => void
}

export default function GenerateButton({ 
  inputText, 
  isGenerating, 
  setIsGenerating 
}: GenerateButtonProps) {
  const [options, setOptions] = useState({
    includeSpeakerNotes: true,
    generateImages: false,
    exportPdf: false,
    theme: 'professional'
  })

  const handleGenerate = async () => {
    if (!inputText.trim()) {
      alert('Please enter some content first')
      return
    }

    setIsGenerating(true)
    try {
      const response = await axios.post(`${API_URL}/generate`, {
        input_text: inputText,
        include_speaker_notes: options.includeSpeakerNotes,
        generate_images: options.generateImages,
        export_pdf: options.exportPdf,
        theme: options.theme
      })

      // Extract filename from file_path
      const filename = response.data.file_path.split('/').pop()
      
      // Download the file
      const downloadUrl = `${API_URL}/download/${filename}`
      window.open(downloadUrl, '_blank')

      alert(`Deck generated successfully! ${response.data.total_slides} slides created.`)
    } catch (error) {
      console.error('Generation error:', error)
      alert('Failed to generate deck. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
      <h3 className="text-xl font-semibold text-primary mb-4">
        Generation Options
      </h3>

      <div className="space-y-4 mb-6">
        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={options.includeSpeakerNotes}
            onChange={(e) => setOptions({...options, includeSpeakerNotes: e.target.checked})}
            className="w-5 h-5 text-secondary rounded focus:ring-secondary"
          />
          <span className="text-gray-700">Include speaker notes</span>
        </label>

        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={options.generateImages}
            onChange={(e) => setOptions({...options, generateImages: e.target.checked})}
            className="w-5 h-5 text-secondary rounded focus:ring-secondary"
          />
          <span className="text-gray-700">Generate images (requires DALL-E)</span>
        </label>

        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={options.exportPdf}
            onChange={(e) => setOptions({...options, exportPdf: e.target.checked})}
            className="w-5 h-5 text-secondary rounded focus:ring-secondary"
          />
          <span className="text-gray-700">Export to PDF</span>
        </label>

        <div>
          <label className="block text-gray-700 mb-2">Theme</label>
          <select
            value={options.theme}
            onChange={(e) => setOptions({...options, theme: e.target.value})}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-transparent"
          >
            <option value="professional">Professional</option>
            <option value="modern">Modern</option>
            <option value="minimal">Minimal</option>
          </select>
        </div>
      </div>

      <button
        onClick={handleGenerate}
        disabled={isGenerating || !inputText.trim()}
        className="w-full bg-primary text-white py-4 rounded-lg font-bold text-lg hover:bg-blue-900 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
      >
        {isGenerating ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating Deck...
          </span>
        ) : (
          '🎯 Generate Deck'
        )}
      </button>
    </div>
  )
}
