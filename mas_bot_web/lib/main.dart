import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'api.dart';
import 'models.dart';

void main() {
  runApp(const MASBotApp());
}

class MASBotApp extends StatelessWidget {
  const MASBotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MAS Chatbot',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo),
      home: const ChatPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final _controller = TextEditingController();
  final List<ChatMessage> _messages = [];
  bool _sending = false;
  late final ApiClient _api;

  @override
  void initState() {
    super.initState();
    _api = ApiClient(
      // dev default; change to your FastAPI public URL when hosted
      baseUrl: const String.fromEnvironment('API_BASE',
          defaultValue: 'http://localhost:8000'),
    );
  }

  Future<void> _send() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _sending) return;
    setState(() {
      _messages.add(ChatMessage(role: Role.user, content: text));
      _sending = true;
    });
    _controller.clear();

    try {
      final reply = await _api.chat(text);
      setState(() {
        _messages.add(ChatMessage(role: Role.assistant, content: reply));
      });
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(
          role: Role.assistant,
          content: '⚠️ Error: $e',
          isError: true,
        ));
      });
    } finally {
      if (mounted) setState(() => _sending = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final spacing = 12.0;
    return Scaffold(
      appBar: AppBar(
        title: const Text('🧠 MAS Bot (Flutter Web)'),
        centerTitle: false,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              separatorBuilder: (_, __) => SizedBox(height: spacing),
              itemBuilder: (context, i) {
                final m = _messages[i];
                final align =
                    m.role == Role.user ? CrossAxisAlignment.end : CrossAxisAlignment.start;
                final bubbleColor = m.isError
                    ? Theme.of(context).colorScheme.errorContainer
                    : (m.role == Role.user
                        ? Theme.of(context).colorScheme.primaryContainer
                        : Theme.of(context).colorScheme.surfaceVariant);

                return Column(
                  crossAxisAlignment: align,
                  children: [
                    Container(
                      constraints: const BoxConstraints(maxWidth: 800),
                      padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 14),
                      decoration: BoxDecoration(
                        color: bubbleColor,
                        borderRadius: BorderRadius.circular(14),
                      ),
                      child: SelectableText(
                        m.content,
                        style: const TextStyle(height: 1.35),
                      ),
                    ),
                  ],
                );
              },
            ),
          ),
          SafeArea(
            top: false,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(12, 8, 12, 12),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      minLines: 1,
                      maxLines: 5,
                      onSubmitted: (_) => _send(),
                      decoration: const InputDecoration(
                        hintText: 'Ask something…',
                        border: OutlineInputBorder(),
                        isDense: true,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  FilledButton.icon(
                    onPressed: _sending ? null : _send,
                    icon: _sending
                        ? const SizedBox(
                            width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                        : const Icon(Icons.send),
                    label: const Text('Send'),
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

