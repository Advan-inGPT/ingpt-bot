enum Role { user, assistant }

class ChatMessage {
  ChatMessage({required this.role, required this.content, this.isError = false});
  final Role role;
  final String content;
  final bool isError;
}

