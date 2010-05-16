#include <clang-c/index.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum CXChildVisitResult foundChild(CXCursor cursor, CXCursor parent, CXClientData client_data)
{
    if(clang_getCursorKind(cursor) == CXCursor_CallExpr)
    {
        printf("-%s\n", clang_getCString(clang_getCursorSpelling(cursor)));
    }

    if(clang_isDeclaration(clang_getCursorKind(cursor)) &&
       clang_getCursorLinkage(cursor) == CXLinkage_External)
    {
        CXFile file;
        const char * filename, * wantFilename;
        CXSourceLocation cloc;

        cloc = clang_getCursorLocation(cursor);
        clang_getInstantiationLocation(cloc, &file, NULL, NULL, NULL);
        filename = clang_getCString(clang_getFileName(file));
        wantFilename = (const char *)client_data;

        if(!filename || strcmp(wantFilename, filename))
            return CXChildVisit_Recurse;

        printf("+%s\n", clang_getCString(clang_getCursorSpelling(cursor)));
    }

    return CXChildVisit_Recurse;
}

int main(int argc, char ** argv)
{
    CXTranslationUnit tu;
    CXIndex idx;
    CXCursor cur;
    char * filename;

    if(argc != 2)
    {
        printf("Usage: %s source_filename.c\n", argv[0]);
        return EXIT_FAILURE;
    }

    filename = argv[1];
    idx = clang_createIndex(1, 1);
    // TODO: fixme, obvious
    char * args[] = {"-I/opt/local/include", "-I/Users/hortont/src/particles/Libraries", "-I/Users/hortont/Desktop/particles"};
    tu = clang_createTranslationUnitFromSourceFile(idx, filename, 3, args, 0, NULL);
    cur = clang_getTranslationUnitCursor(tu);

    clang_visitChildren(cur, foundChild, strdup(filename));

    return EXIT_SUCCESS;
}
