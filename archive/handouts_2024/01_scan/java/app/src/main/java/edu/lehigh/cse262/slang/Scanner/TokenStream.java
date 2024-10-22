package edu.lehigh.cse262.slang.Scanner;

import java.util.List;

/**
 * TokenStream is a wrapper around a list of tokens. The reason for the wrapper
 * is that our Parser won't be able to just iterate through the tokens, because
 * many of the grammar's productions require a little bit of look-ahead (one or
 * two tokens). TokenStream provides an API that is easy enough to iterate
 * through, but which is also friendly to the requirements of the Parser.
 */
public class TokenStream {
    /**
     * A collection of tokens, in the order they were observed in the source
     * file
     */
    private final List<Tokens.BaseToken> tokens;

    /**
     * A lightweight iterator mechanism: this int just tells which entry in
     * tokens to return next.
     */
    private int next = 0;

    /** Construct a ScanResult from a list of tokens */
    public TokenStream(List<Tokens.BaseToken> tokens) {
        this.tokens = tokens;
    }

    /** Reset the iterator, so that we can iterate through the tokens */
    public void reset() {
        this.next = 0;
    }

    /** Get the next token, via the iterator-like interface */
    public Tokens.BaseToken nextToken() {
        return (!hasNext()) ? null : tokens.get(next);
    }

    /** Get the token after the next token, via the iterator-like interface */
    public Tokens.BaseToken nextNextToken() {
        return (!hasNextNext()) ? null : tokens.get(next + 1);
    }

    /** Pop a token off the stack */
    public void popToken() {
        ++next;
    }

    /** Report if there is more for the iterator to consume */
    public boolean hasNext() {
        return next < tokens.size();
    }

    /** Report if there is even more for the iterator to consume */
    public boolean hasNextNext() {
        return (next + 1) < tokens.size();
    }
}