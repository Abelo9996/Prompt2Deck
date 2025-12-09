# Sample Inputs for Prompt2Deck

This file contains example inputs you can use to test the Prompt2Deck generator.

## Example 1: Simple Topic

```
Explain Large Language Models
```

This will generate a basic slide deck with an introduction, key concepts, applications, and conclusion.

---

## Example 2: Bullet List

```
Introduction to Machine Learning
* Supervised Learning
* Unsupervised Learning
* Reinforcement Learning
* Neural Networks
* Real-world Applications
```

Each bullet will become a slide with expanded content.

---

## Example 3: Nested Outline

```
Introduction to Cloud Computing

1. What is Cloud Computing?
   - Definition
   - Key characteristics
   - Evolution of cloud services

2. Cloud Service Models
   - Infrastructure as a Service (IaaS)
   - Platform as a Service (PaaS)
   - Software as a Service (SaaS)

3. Major Cloud Providers
   - Amazon Web Services (AWS)
   - Microsoft Azure
   - Google Cloud Platform

4. Benefits and Challenges
   - Cost efficiency
   - Scalability
   - Security considerations
   - Vendor lock-in

5. Conclusion
   - Future of cloud computing
   - Getting started
```

This creates a structured presentation with main topics and sub-bullets.

---

## Example 4: Technical Presentation

```
Building Microservices Architecture

Introduction
- Monolithic vs Microservices
- When to use microservices

Core Principles
- Single Responsibility
- Decentralization
- Fault Isolation

Key Technologies
- Docker and Containers
- Kubernetes
- Service Mesh
- API Gateways

Best Practices
- Database per service
- Event-driven communication
- Monitoring and observability

Challenges
- Distributed system complexity
- Data consistency
- Testing strategies

Getting Started
- Start small
- Incremental migration
- Tools and frameworks
```

---

## Example 5: Business Presentation

```
Q4 Product Launch Strategy

* Executive Summary
* Market Analysis
* Target Audience
* Product Features
* Go-to-Market Strategy
* Marketing Channels
* Timeline and Milestones
* Budget and Resources
* Success Metrics
* Next Steps
```

---

## Example 6: Educational Content

```
Understanding Photosynthesis

What is Photosynthesis?
- Energy conversion process
- Occurs in plants and algae

The Process
- Light-dependent reactions
- Light-independent reactions (Calvin Cycle)
- Role of chlorophyll

Inputs and Outputs
- Carbon dioxide + Water + Light
- Glucose + Oxygen

Importance
- Oxygen production
- Food chain foundation
- Carbon cycle regulation

Conclusion
- Essential for life on Earth
```

---

## Tips for Best Results

1. **Be Clear**: Use descriptive titles and clear bullet points
2. **Structure Matters**: Use indentation to show hierarchy
3. **Keep it Concise**: 5-10 slides is ideal for most presentations
4. **Topic-Based**: For simple topics, let the AI generate the structure
5. **Outline-Based**: For specific content, provide a detailed outline

---

## Testing via API

### Preview Request

```bash
curl -X POST http://localhost:8000/preview \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Explain Machine Learning\n* Supervised Learning\n* Unsupervised Learning\n* Applications",
    "include_speaker_notes": true
  }'
```

### Generate Deck Request

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Introduction to AI",
    "include_speaker_notes": true,
    "generate_images": false,
    "export_pdf": false,
    "theme": "professional"
  }'
```
