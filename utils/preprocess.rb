class Post
    def initialize(filename)
        @file = File.new(filename, "r")
        @current_char = ""
        @previous_char = nil
        @current_index = 0 # eagerly points to the next element to be consumed
        @current_tag = nil
    end

    def _advance()

    end

    def fix_math:
        # Spots $latex ...$ and substitutes it by $...$ with the exception of centered math (display)
        @file.each_line do |line|
            line.each_char do |char|
                case char
                when "$"
                    
                end
            end
        end
    end

    def rows
        count = 0
        @file.each_line do |line|
            count += 1
        end
        return count
    end
end

if __FILE__ == $0
    PATH = File.expand_path File.dirname(__FILE__)
    POSTS_PATH = File.join(PATH, "_posts")
    puts "CWD: #{POSTS_PATH}"
    
    posts_processed = 0
    Dir.foreach(POSTS_PATH) do |filename|
        next if filename == "." or filename == ".."
        post = Post.new(File.join(POSTS_PATH, filename))
        print "Post rows: #{post.rows}\r"
        posts_processed += 1
    end
    puts "Posts processed: #{posts_processed}."
end