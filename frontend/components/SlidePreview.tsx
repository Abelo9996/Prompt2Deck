interface SlidePreviewProps {
  previewData: any
}

export default function SlidePreview({ previewData }: SlidePreviewProps) {
  if (!previewData) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        <div className="text-center">
          <svg
            className="mx-auto h-12 w-12 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <p>Preview will appear here</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4 max-h-96 overflow-y-auto">
      <div className="text-sm text-gray-600 mb-4">
        {previewData.total_slides} slides total
      </div>

      {previewData.slides.map((slide: any, index: number) => (
        <div
          key={index}
          className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
        >
          <div className="flex items-start justify-between mb-2">
            <h3 className="font-semibold text-primary flex-1">
              {index + 1}. {slide.title}
            </h3>
          </div>

          {slide.bullets && slide.bullets.length > 0 && (
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-700 ml-2">
              {slide.bullets.map((bullet: string, i: number) => (
                <li key={i}>{bullet}</li>
              ))}
            </ul>
          )}

          {slide.speaker_notes && (
            <div className="mt-3 pt-3 border-t border-gray-100">
              <p className="text-xs text-gray-500 italic">
                Notes: {slide.speaker_notes}
              </p>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
