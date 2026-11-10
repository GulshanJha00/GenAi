class Transformer:
    def encoder(self,text):
        words = text.split()
        counter = 0
        vocab = {}
        for word in words:
            if word not in vocab:
                vocab[word] = counter
                counter += 1
        return vocab

    def decoder(self, vocab, encoded):
        reverse_vocab = {}

        for i, j in vocab.items():
            reverse_vocab[j] = i

        text = ""

        for i in encoded:
            word = reverse_vocab[i]
            text = text + word + " "
        return text



text = 'Hello this is text my friend'
transformer = Transformer()
vocab = transformer.encoder(text)
encoded = [1, 2, 3, 4, 5, 2, 3, 4, 5]
decode = transformer.decoder(vocab, encoded)
print(decode)