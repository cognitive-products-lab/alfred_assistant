# Rapport ALFRED vs dashboard_manifest_target_v1.json

## B01 -- Interaction conversationnelle

- OK Code partiel -- src/main.py
- OK Code partiel -- src/__init__.py
- OK Code partiel -- src/conversation/input/audio_capture.py
- OK Code partiel -- src/conversation/input/text_input.py
- OK Code partiel -- src/conversation/input/context_builder.py
- OK Code partiel -- src/conversation/nlp/nlp_engine_v2.py
- OK Code partiel -- src/conversation/input/speech_manager.py
- OK Code partiel -- src/conversation/input/stt_whisper.py
- OK Code partiel -- src/conversation/input/voice_profile.py
- OK A coder -- src/conversation/input/__init__.py
- OK Code partiel -- src/conversation/output/tts_output.py
- OK Code partiel -- src/conversation/output/tts_piper.py
- OK A coder -- src/conversation/output/__init__.py
- OK Code partiel -- src/conversation/input/audio_listener.py
- OK Code partiel -- src/conversation/nlp/intent_classifier.py
- OK Code partiel -- src/conversation/output/tts_engine.py
- OK Code partiel -- src/conversation/__init__.py
- OK Code partiel -- src/llm/llm_client_openai.py
- OK Code partiel -- src/llm/llm_client_ollama.py
- OK A coder -- src/llm/__init__.py
- OK Code partiel -- src/core/response_generator.py
- OK Code partiel -- config/conversation_rules.json
- OK Code partiel -- config/intents_catalog.json
- OK Code partiel -- config/response_patterns.json
- OK Code partiel -- data/dialogue_history.json
- OK Code partiel -- tests/test_b01_speech.py
- OK Code partiel -- tests/test_pipeline.py

## B02 -- Memoire et RAG

- OK Code partiel -- src/memory/memory_manager.py
- OK Code partiel -- src/memory/episodic_memory.py
- OK Code partiel -- src/memory/long_term_memory.py
- OK Code partiel -- src/memory/memory_indexer.py
- OK Code partiel -- src/memory/rag_stub.py
- OK A coder -- src/memory/__init__.py
- OK Code partiel -- src/rag/rag_engine.py
- OK Code partiel -- src/rag/__init__.py
- OK Code partiel -- src/rag/__init__.py
- OK Code partiel -- config/rag_settings.json
- OK Code partiel -- config/knowledge_settings.json
- OK Code partiel -- data/user_memory.json
- OK Code partiel -- data/memory/episodic/dialogue_history.json
- OK Code partiel -- knowledges/system/memory/memory_system.json
- OK Code partiel -- knowledges/system/memory/episodic_memory.json
- OK Code partiel -- tests/test_b02_b03.py

## B03 -- Emotions et Regulation

- OK Code partiel -- src/regulation/emotion_detector.py
- OK Code partiel -- src/regulation/mode_manager.py
- OK Code partiel -- src/regulation/protection_guard.py
- OK Code partiel -- src/regulation/wellbeing_tracker.py
- OK A coder -- src/regulation/__init__.py
- OK Code partiel -- config/v2/emotion_profiles.json
- OK Code partiel -- knowledges/human/emotional_intelligence/emotional_support.json
- OK Code partiel -- knowledges/human/emotional_intelligence/empathy.json
- OK Code partiel -- knowledges/human/psychology/resilience.json
- OK Code partiel -- knowledges/lifestyle/health/stress_management.json

## B04 -- Securite et Protection

- OK Code partiel -- .env
- OK Code partiel -- .env.example
- OK Code partiel -- .gitignore
- OK Code partiel -- config/ethics_rules.json
- OK Code partiel -- config/quality_thresholds.json
- OK Code partiel -- config/settings.json
- OK Code partiel -- config/safety_rules.json
- OK Code partiel -- pyproject.toml
- OK Code partiel -- knowledges/system/ethics/ethical_framework.json

## B05 -- Organisation et Assistance

- OK Code partiel -- src/assistant_actions/__init__.py
- OK Code partiel -- data/actions/tasks.json
- OK Code partiel -- knowledges/cpl/execution/task_prioritization.json
- OK Code partiel -- knowledges/cpl/execution/project_management_core.json
- OK Code partiel -- knowledges/lifestyle/daily_life/time_management.json

## B06 -- Communication et Lien social

- OK Code partiel -- knowledges/cpl/human_communication/communication_principles.json
- OK Code partiel -- knowledges/cpl/human_communication/client_interaction.json
- OK Code partiel -- knowledges/human/skills/softskills/communication.json
- OK Code partiel -- knowledges/human/skills/softskills/assertiveness.json

## B07 -- Mobilite et Contexte externe

- OK Code partiel -- data/context/user_context.json

## B08 -- Personnalisation utilisateur

- OK Code partiel -- src/core/personality_adapter.py
- OK Code partiel -- src/core/alfred_behavior_engine.py
- OK Code partiel -- src/core/__init__.py
- OK Code partiel -- config/personality_core.json
- OK Code partiel -- config/behavior_rules_softskills.json
- OK Code partiel -- config/user_adaptation_profile.json
- OK Code partiel -- data/personality/instances/personality_core_instance.json
- OK Code partiel -- data/personality/templates/personality_core.json
- OK Code partiel -- data/profile/user_profile.json
- OK Code partiel -- data/users/instances/user_celine_instance.json
- OK Code partiel -- data/preferences_profile.json
- OK Code partiel -- knowledges/core/alfred_core_identity.json
- OK Code partiel -- knowledges/core/behavioral_modes.json
- OK Code partiel -- knowledges/core/context_awareness.json
- OK Code partiel -- knowledges/core/personalization_engine.json
- OK Code partiel -- knowledges/core/system_rules.json
- OK Code partiel -- knowledges/core/user_adaptation.json

## B15 -- Presence visuelle et Avatar

- OK Code partiel -- src/ui/__init__.py
- OK Code partiel -- assets/avatar/base/avatar_mouth_a_eyes_open.png.png
- OK Code partiel -- assets/avatar/base/avatar_mouth_idle_eyes_open.png.png
- OK Code partiel -- assets/avatar/base/avatar_mouth_o_eyes_open.png.png
- OK Code partiel -- assets/voices/fr_FR-upmc-medium.onnx
- OK Code partiel -- assets/voices/fr_FR-upmc-medium.onnx.json
- OK Code partiel -- speech/tts/models/fr_FR/fr_FR-upmc-medium.onnx
- OK Code partiel -- speech/tts/models/fr_FR/fr_FR-upmc-medium.onnx.json

## B18 -- Knowledge et Intelligence System

- OK Code partiel -- src/knowledge/knowledge_loader.py
- OK Code partiel -- src/knowledge/knowledge_router.py
- OK Code partiel -- src/knowledge/__init__.py
- OK Code partiel -- ALFRED_CONTEXT.md
- OK Code partiel -- README.md
- OK Code partiel -- bootstrap_project.ps1
- OK Code partiel -- paths.py
- OK Code partiel -- requirements.txt
- OK Code partiel -- config/alfred_project.json
- OK Code partiel -- config/v1/basic_pipeline_rules.json
- OK Code partiel -- config/router_rules.json
- OK Code partiel -- config/routing_rules.json
- OK Code partiel -- knowledges/knowledge_registry.json
- OK Code partiel -- knowledges/manifest.json
- OK Code partiel -- knowledges/taxonomy.json
- OK Code partiel -- knowledges/cpl/strategy/strategy_fundamentals.json
- OK Code partiel -- knowledges/cpl/product_ia/product_design_methodology.json
- OK Code partiel -- knowledges/professional/engineering/ai/llm_basics.json
- OK Code partiel -- knowledges/professional/engineering/ai/rag.json
- OK Code partiel -- knowledges/human/psychology/motivation.json
- OK Code partiel -- knowledges/human/cognition/focus_management.json
- OK Code partiel -- src/v1/__init__.py
- OK A coder -- tests/__init__.py

## B20 -- Cybersecurite Zero Trust

- OK Code partiel -- src/security/zero_trust_orchestrator.py
- OK Code partiel -- src/security/threat_detector.py
- OK Code partiel -- src/security/session_manager.py
- OK Code partiel -- src/security/security_logger.py
- OK Code partiel -- src/security/security_config.py
- OK Code partiel -- src/security/role_manager.py
- OK Code partiel -- src/security/quarantine_service.py
- OK Code partiel -- src/security/prompt_guard.py
- OK Code partiel -- src/security/policy_engine.py
- OK Code partiel -- src/security/policy_enforcement_point.py
- OK Code partiel -- src/security/policy_decision_point.py
- OK Code partiel -- src/security/permission_manager.py
- OK Code partiel -- src/security/output_filter.py
- OK Code partiel -- src/security/mfa_manager.py
- OK Code partiel -- src/security/input_validator.py
- OK Code partiel -- src/security/incident_manager.py
- OK Code partiel -- src/security/encryption_service.py
- OK Code partiel -- src/security/device_registry.py
- OK Code partiel -- src/security/compliance_manager.py
- OK Code partiel -- src/security/behavioral_detector.py
- OK Code partiel -- src/security/backup_security.py
- OK Code partiel -- src/security/audit_trail.py
- OK Code partiel -- src/security/access_control.py
- OK Code partiel -- src/security/secret_manager.py
- OK A coder -- src/security/__init__.py
- OK Code partiel -- config/security/access_policies.json
- OK Code partiel -- config/security/audit_retention_policy.json
- OK Code partiel -- config/security/roles_permissions.json
- OK Code partiel -- config/security/security_settings.json
- OK Code partiel -- config/security/trusted_devices.json
- OK Code partiel -- config/security/zero_trust_rules.json
- OK Code partiel -- data/security/access_decisions_history.json
- OK Code partiel -- data/security/incident_register.json
- OK Code partiel -- data/security/trusted_devices_runtime.json
- OK Code partiel -- knowledges/professional/engineering/cybersecurite/cybersecurity_core.json
- OK Code partiel -- knowledges/professional/engineering/cybersecurite/rgpd_core.json
- OK Code partiel -- logs/security/security.log
