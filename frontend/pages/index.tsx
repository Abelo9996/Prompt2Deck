import { useState } from 'react'
import Head from 'next/head'
import InputForm from '../components/InputForm'
import SlidePreview from '../components/SlidePreview'
import GenerateButton from '../components/GenerateButton'

export default function Home() {
  const [inputText, setInputText] = useState('')
  const [previewData, setPreviewData] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)

  return (
    <>
      <Head>
        <title>Prompt2Deck - AI Slide Deck Generator</title>
        <meta name="description" content="Generate professional slide decks from text using AI" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-12">
          <header className="text-center mb-12">
            <h1 className="text-5xl font-bold text-primary mb-4">
              Prompt2Deck
            </h1>
            <p className="text-xl text-gray-600">
              Transform your ideas into professional slide decks with AI
            </p>
          </header>

          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Input Section */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-semibold text-primary mb-4">
                  Input
                </h2>
                <InputForm
                  inputText={inputText}
                  setInputText={setInputText}
                  setPreviewData={setPreviewData}
                  isGenerating={isGenerating}
                />
              </div>

              {/* Preview Section */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-semibold text-primary mb-4">
                  Preview
                </h2>
                <SlidePreview previewData={previewData} />
              </div>
            </div>

            {/* Generate Button */}
            <div className="mt-8 text-center">
              <GenerateButton
                inputText={inputText}
                isGenerating={isGenerating}
                setIsGenerating={setIsGenerating}
              />
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
